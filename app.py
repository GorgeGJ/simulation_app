import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pillar Contribution Simulator", layout="wide")
st.title("📊 Pillar Contribution Simulator")

pillar_file = st.file_uploader("Upload Pillar Inputs CSV", type=["csv"])
channel_file = st.file_uploader("Upload Channel Contributions CSV", type=["csv"])

def simulate_pillar_contribution(merged_df):
    event_sum = merged_df.groupby(["week", "channel"])["event"].transform("sum")
    merged_df["channel_effectiveness"] = merged_df["contribution"] / event_sum

    pillar_weights = []
    for channel, group in merged_df.groupby("channel"):
        try:
            X = group[["event"]].values
            y = group["contribution"].values
            coef = LinearRegression().fit(X, y).coef_[0] if len(np.unique(X)) > 1 else 1.0
        except Exception:
            coef = 1.0
        pillar_weights.append((channel, coef))

    weight_df = pd.DataFrame(pillar_weights, columns=["channel", "raw_weight"])
    scaler = MinMaxScaler(feature_range=(0.7, 1.3))
    weight_df["pillar_weight"] = scaler.fit_transform(weight_df[["raw_weight"]])

    merged_df = pd.merge(merged_df, weight_df[["channel", "pillar_weight"]], on="channel", how="left")

    merged_df["pillar_contribution"] = (
        merged_df["event"] * merged_df["channel_effectiveness"] * merged_df["pillar_weight"]
    )

    return merged_df

if pillar_file and channel_file:
    df_pillar = pd.read_csv(pillar_file)
    df_channel = pd.read_csv(channel_file)

    st.subheader("📂 Uploaded Data Preview")
    st.write("Pillar Inputs", df_pillar.head())
    st.write("Channel Contributions", df_channel.head())

    merged_df = pd.merge(df_pillar, df_channel, on=["week", "channel"], how="inner")

    st.subheader("⚙️ Simulating Pillar Contributions...")
    merged_df = simulate_pillar_contribution(merged_df)

    pillar_output = merged_df.groupby(["week", "pillar", "channel"])[["pillar_contribution", "event", "spend"]].sum().reset_index()
    st.success("✅ Simulation complete!")

    def convert_df(df):
        output = BytesIO()
        df.to_csv(output, index=False)
        return output.getvalue()

    st.subheader("📥 Download Simulated Pillar Contribution")
    st.download_button(
        label="Download CSV",
        data=convert_df(pillar_output),
        file_name="simulated_pillar_contribution.csv",
        mime="text/csv"
    )

    st.write("Preview of Simulated Output:")
    st.dataframe(pillar_output)

    st.subheader("📈 Pillar Contribution Trend Over Time")

    unique_pillars = pillar_output["pillar"].unique()
    unique_channels = pillar_output["channel"].unique()
    unique_weeks = sorted(pillar_output["week"].unique())

    selected_pillar = st.selectbox("Select a pillar:", unique_pillars)
    selected_metric = st.radio("Choose a metric to chart:", ["pillar_contribution", "event", "spend"])
    selected_channels = st.multiselect("Filter by channel(s):", unique_channels, default=unique_channels)
    week_range = st.slider("Select week range:", min_value=min(unique_weeks), max_value=max(unique_weeks),
                           value=(min(unique_weeks), max(unique_weeks)))

    filtered_df = pillar_output[
        (pillar_output["pillar"] == selected_pillar) &
        (pillar_output["channel"].isin(selected_channels)) &
        (pillar_output["week"] >= week_range[0]) &
        (pillar_output["week"] <= week_range[1])
    ]

    chart_df = filtered_df.groupby("week")[[selected_metric]].sum().reset_index().sort_values("week")

    st.line_chart(chart_df.set_index("week"))

    fig, ax = plt.subplots()
    ax.plot(chart_df["week"], chart_df[selected_metric], marker="o", linewidth=2)
    ax.set_title(f"{selected_metric.replace('_', ' ').title()} Trend for '{selected_pillar}'")
    ax.set_xlabel("Week")
    ax.set_ylabel(selected_metric.replace("_", " ").title())
    ax.grid(True)
    st.pyplot(fig)

    img_buffer = BytesIO()
    fig.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    st.download_button(
        label="📤 Download Chart as PNG",
        data=img_buffer,
        file_name=f"{selected_pillar}_{selected_metric}_trend.png",
        mime="image/png"
    )
