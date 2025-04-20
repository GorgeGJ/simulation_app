# 📊 Pillar Contribution Simulator

A lightweight Streamlit app that helps simulate and visualize **pillar-level marketing contributions** from user-uploaded CSV files. Built for data scientists and marketers to better understand how media inputs drive value across different marketing pillars.

## 🚀 Features

- 📂 Upload **Pillar Inputs** and **Channel Contribution** CSVs
- 🔄 Merge and simulate contribution using:
  - Event volumes
  - Channel effectiveness (normalized by total weekly events)
  - Regression-derived pillar weight per channel
- 📊 View interactive **trend charts** by pillar, channel, and week
- 📥 Download simulated output as **CSV**
- 🖼 Export charts as **PNG images**

## 📁 Input File Formats

### 🧱 Pillar Inputs CSV
| week | pillar | channel | event | spend |
|------|--------|---------|--------|--------|

### 🔌 Channel Contribution CSV
| week | channel | contribution |
|------|---------|--------------|

## 🛠 How It Works

The app performs a 3-step simulation:

1. **Channel Effectiveness** = contribution ÷ total events for that channel in a week  
2. **Pillar Weight** = regression coefficient between `event` and `contribution` for each channel, normalized to `[0.7, 1.3]`  
3. **Pillar Contribution** = event × channel effectiveness × pillar weight

## 🧪 Try It Locally

```bash
git clone https://github.com/your-username/pillar-contribution-app.git
cd pillar-contribution-app
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Live App

> [🔗 Click here to launch the app on Streamlit Cloud]((https://simulationapp-9wgnjks7jfekhtg5k3mmwo.streamlit.app))

## 📦 Requirements

```txt
streamlit
pandas
numpy
scikit-learn
matplotlib
```

## ✨ Future Improvements

- Add support for weekly time-series forecasting
- Upload zipped input templates
- Save sessions with historical simulations
- Enhanced charting with Plotly

## 📬 Feedback & Contributions

Have ideas or bugs to report? Open an issue or submit a PR!
