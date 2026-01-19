# 📈 **Trendly - AI Stock Analysis Platform**

### **Advanced ML Ensemble • Exit Timing • Lenient Recommendations • 35+ Technical Indicators**

**Trendly is a sophisticated machine learning application that analyzes 450+ S&P 500 stocks using ensemble AI models. Combining RandomForest, GradientBoosting, and AutoReg with 35+ technical indicators, it delivers institutional-grade predictions with confidence scores, exit timing analysis, and actionable insights.**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40.1-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌟 **What's New in v4.2**

### Exit Timing & Lenient Recommendations

- ⏰ **Exit Timing Analysis** - Know when to sell before downtrends (NEW!)
  - Detects peaks in forecast predictions
  - 3 signal types: HOLD (🟢), WATCH (🟡), EXIT (🔴)
  - Confidence scoring for exit signals (0-100%)
  - Optimal exit date recommendations

- 🚀 **Lenient Return-Based Recommendations** - Focus on "will it go up?" (IMPROVED!)
  - Strong Buy: Predicted return > 2.0%
  - Buy: Predicted return > 0.5%
  - Hold: -0.5% to 0.5%
  - Much more user-friendly than previous system

- � **Terminology Guide** - Understand all metrics (NEW!)
  - Expandable glossary in app
  - 9 comprehensive term explanations
  - Real-world examples for each indicator

---

## 🌟 **What's New in v4.1**

### Smart Investment Recommendation

- 🎯 **"What Should I Invest In?" Button** - AI analyzes top 10 stocks and recommends the best opportunity
  - Compares multiple stocks simultaneously
  - Shows confidence scores and predicted returns
  - Displays top 5 alternatives with detailed breakdowns
  - One-click analysis of recommended stock

---

## 🌟 **What's New in v4.0 - Advanced ML Upgrade**

### Revolutionary ML System

- 🤖 **Ensemble Machine Learning** - Combines RandomForest + GradientBoosting + AutoReg

- 📊 **35+ Technical Indicators** - RSI, MACD, Bollinger Bands, ATR, OBV, Stochastic, EMA, Golden Cross

- 🎯 **Model Confidence Scores** - Know when to trust predictions (0-100% confidence)

- 🔬 **6-Component Scoring** - Return (35pts), Trend (25pts), Risk (15pts), Volume (10pts), Technicals (10pts), Confidence (5pts)

- 📈 **5-Tier Recommendations** - Strong Buy, Buy, Hold, Cautious, Sell

- ⚡ **Advanced Pattern Recognition** - Support/Resistance, Golden/Death Cross, OB/OS detection

- 📉 **Model Performance Metrics** - MAE and R² scores displayed for transparency

- 💡 **Smart Insights** - 10+ types of intelligent reasoning with emoji indicators

### Key Improvements

- **Accuracy**: Ensemble reduces prediction error by 15-30%
- **Reliability**: Multi-model consensus with confidence scoring
- **Depth**: 35+ indicators vs 8 previously
- **Precision**: 6-component scoring vs 4 previously
- **Intelligence**: Context-aware recommendations with technical analysis



- 📈 **5-Tier Recommendations** - Strong Buy (≥70), Buy (60-69), Hold (45-59), Cautious (30-44), Sell (<30)[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)

[![Streamlit](https://img.shields.io/badge/Streamlit-1.40.1-red.svg)](https://streamlit.io/)

---[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



## 🧬 **Project Structure**---

```bash

Trendly/## 🌟 **What's New in v3.0 - Major UI Overhaul**

├── README.md                             # This file

├── LICENSE                               # MIT License### No Sidebar, More Features

├── requirements.txt                      # Python dependencies- � **Sidebar Completely Removed** - Clean, single-page experience

├── .gitignore                           # Git ignore rules- 🎨 **Hero Header** - Large gradient banner with prominent Trendly branding

├── streamlit_app/                       # Main application- 📊 **Live Stats Bar** - Real-time market status, 450+ stock count, current time, AI badge

│   ├── 00_ℹ️_Info.py                    # Main dashboard- ⚡ **Quick Stock Buttons** - One-click access to AAPL, MSFT, NVDA, TSLA

│   ├── modules/- 📈 **Enhanced Score Card** - 84px dynamic gradient display with pulse animation

│   │   └── helper.py                     # ML & analysis functions- 🎯 **Better Scoring** - Realistic thresholds (BUY ≥60, HOLD 35-59, SELL <35)

│   └── pages/               - � **Improved Charts** - Area fills, dashed predictions, diamond markers, unified tooltips

│       └── 01_📈_Investment_Analyzer.py  # Alternative analyzer- � **Key Takeaways** - Two-column summary with positive signals & considerations

├── assets/                              # Data files- ✨ **Feature Highlights** - Beautiful cards showcasing ML, Real-Time Data, Clear Insights

│   └── data/- 🎨 **Modern Design** - Gradients, animations, hover effects, professional typography

│       └── sp500_tickers.csv             # S&P 500 stock list

├── docs/                                 # Documentation---

│   ├── ADVANCED_ML_UPGRADE.md

│   ├── BEFORE_AFTER_COMPARISON.md## 🧬 **Project Structure**

│   ├── QUICK_REFERENCE.md```bash

│   └── ... (other docs)Trendly/

└── venvStreamlit311/                     # Python virtual environment├── streamlit_app/

```│   ├── 00_ℹ️_Info.py                    # Landing page with info & navigation

│   ├── modules/

---│   │   └── helper.py                     # Core analysis functions

│   └── pages/               

## 🚀 **Quick Start**│       └── 01_📈_Investment_Analyzer.py  # Main analyzer with sidebar controls

├── assets/         

### 1. Clone the Repository│   └── data/

```bash│       └── sp500_tickers.csv             # S&P 500 stock list

git clone <repository-url>├── venvStreamlit311/                     # Python 3.11 environment

cd Trendly├── LICENSE                 

```├── README.md                             # This file

├── requirements.txt                      # Dependencies

### 2. Create Virtual Environment├── INVESTMENT_SYSTEM_GUIDE.md            # Complete methodology guide

```bash├── UI_IMPROVEMENTS.md                    # UI enhancement documentation

python3.11 -m venv venvStreamlit311├── VISUAL_GUIDE.md                       # Quick visual reference

source venvStreamlit311/bin/activate  # On macOS/Linux├── DEFEAT_BETA_MIGRATION.md              # API migration notes

```└── FINAL_UPDATE_SUMMARY.md               # Latest updates summary

```

### 3. Install Dependencies

```bash---

pip install -r requirements.txt

```## 🛠️ **Technology Stack**



### 4. Run the Application### Core Technologies

```bash- **Streamlit 1.40.1** - Web framework

cd streamlit_app- **Defeat Beta API 0.0.29** - Real-time market data (no API key, no limits)

streamlit run "00_ℹ️_Info.py"- **Statsmodels 0.14.0** - AutoReg time-series model

```- **Plotly 5.17.0** - Interactive visualizations

- **Python 3.11** - Latest stable Python

The app will open at `http://localhost:8501`

### Key Libraries

---- **Pandas 2.2.3** - Data manipulation

- **NumPy 2.4.1** - Numerical computing

## 🎯 **Key Features**- **DuckDB** - Fast analytical queries

- **Hugging Face** - Dataset access

### 🎯 **Smart Investment Recommendation**

Click "What Should I Invest In?" to get AI-powered recommendations:---

- Analyzes top 10 stocks automatically

- Compares scores, confidence, and predicted returns## 🎯 **Features**

- Shows top 5 alternatives

- One-click deep dive### 🔍 **Smart Analysis**

- Multi-factor scoring system (0-100)

### 🤖 **Advanced ML Analysis**- ML-powered price predictions

- Ensemble predictions (3 models)- Real-time market data

- Confidence scores (0-100%)- 15+ technical indicators

- 35+ technical indicators

- Real-time market data### 📊 **Clear Insights**

- Color-coded recommendations (Buy/Hold/Sell)

### 📊 **Comprehensive Insights**- Visual risk level indicators

- 5-tier recommendations (Strong Buy to Sell)- Trend strength analysis

- Golden Cross detection- Volume confirmation

- RSI, MACD, Bollinger Bands

- Volume confirmation with OBV### 🚀 **Easy to Use**

- Intuitive sidebar controls

---- 3-step workflow

- No technical knowledge required

## 📊 **Understanding Scores**- Beautiful, modern interface

- Export capabilities (CSV download)

### Investment Score (0-100)

- **70-100**: 🚀 Strong Buy---

- **60-69**: ✅ Buy

- **45-59**: ⚠️ Hold## 🧑‍💻 **How It Works**

- **30-44**: ⚡ Cautious

- **0-29**: ❌ Sell### Two-Phase System:



### Model Confidence (0-100%)#### Phase 1: Machine Learning Prediction

- **80-100%**: Very High - Trust it1. User selects a stock ticker from the S&P 500 list

- **60-79%**: High - Reliable2. Historical stock data is retrieved using Defeat Beta API (powered by DuckDB & Hugging Face)

- **40-59%**: Moderate - Be cautious3. Comprehensive features are engineered:

- **<40%**: Low - Verify with other sources   - Past prices (memory of the market)

   - Moving averages (trend detection)

---   - Momentum indicators (price velocity)

   - Volatility measures (risk awareness)

## 🛠️ **Technology Stack**   - Volume indicators (market confidence)

4. AutoReg model is trained on 2 years of historical data

- **Streamlit 1.40.1** - Web framework5. Model generates predictions for the next 5–180 days

- **scikit-learn** - ML models

- **Statsmodels** - Time series#### Phase 2: Investment Scoring & Recommendation

- **ta** - Technical indicators6. System calculates Investment Score (0-100) based on:

- **Plotly** - Visualizations   - **Expected Return (0-40 points)**: Predicted profit potential

- **Defeat Beta API** - Market data   - **Trend Strength (0-30 points)**: Price position vs moving averages

- **Python 3.11**   - **Risk Level (0-20 points)**: Volatility analysis

   - **Volume Confirmation (0-10 points)**: Market participation

---7. Clear recommendation is generated:

   - ✅ **Invest** (Score: 70-100)

## 📚 **Documentation**   - ⚠️ **Hold/Wait** (Score: 40-69)

   - ❌ **Do Not Invest** (Score: 0-39)

Detailed guides in `/docs`:8. Detailed reasoning and breakdown are provided

- `ADVANCED_ML_UPGRADE.md` - ML system details

- `QUICK_REFERENCE.md` - Indicator guide---

- `BEFORE_AFTER_COMPARISON.md` - Version comparison

## ✨ **Key Features**

---

### 🎯 Investment Analysis

## ⚠️ **Disclaimer**- **Multi-Factor Investment Scoring** - Comprehensive 0-100 scoring system

- **Clear Buy/Hold/Sell Recommendations** - Actionable investment decisions

**For EDUCATIONAL PURPOSES ONLY. Not financial advice.**- **Detailed Score Breakdown** - Transparency in how scores are calculated

- **Risk-Adjusted Analysis** - Balances return potential with volatility

- Markets are risky and unpredictable

- Past performance ≠ future results### 📊 Data & Predictions

- Always consult qualified financial advisors- **Real-time S&P 500 stock data** - Access accurate and up-to-date information

- Never invest more than you can afford to lose- **No API keys or rate limits** - Powered by Defeat Beta API

- **Custom prediction ranges** - Forecast stock prices for 5 to 180 days

---- **Interactive visualizations** - View historical trends and future predictions



## 📝 **License**### 📈 Technical Indicators

- **Moving Averages** - 5, 10, and 20-day trend analysis

MIT License - see [LICENSE](LICENSE) file- **Momentum Indicators** - Daily returns and price changes

- **Volatility Measures** - Risk assessment through standard deviation

---- **Volume Analysis** - Market confidence indicators



## 🎯 **Roadmap**### 💡 User Experience

- **Professional Dashboard** - Clean, intuitive interface

Coming in v5.0:- **Detailed Explanations** - Understand the reasoning behind recommendations

- Portfolio optimization- **Educational Disclaimers** - Responsible investing guidance

- Sector comparison- **Responsive Design** - Works on desktop and mobile devices

- News sentiment analysis

- Real-time alerts---

- Dark mode theme

## 🚀 **Getting Started**

---

### **Local Installation**

**Built with ❤️ by the Trendly Team**

1. Clone the repository:

**Trendly v4.1: Where AI Meets Wall Street** 🚀📈```bash

git clone https://github.com/user/SP500Forecaster.git
```
**Hint:** Replace `user` with `josericodata` in the URL above. I am deliberately asking you to pause here so you can support my work. If you appreciate it, please consider giving the repository a star or forking it. Your support means a lot—thank you! 😊

2. Navigate to the repository directory:
```bash
cd SP500Forecaster
```

3. Create a virtual environment:
```bash
python3 -m venv venvStreamlit
```

4. Activate the virtual environment:
```bash
source venvStreamlit/bin/activate
```

5. Install requirements:
```bash
pip install -r requirements.txt
```

6. Navigate to the app directory:
```bash
cd streamlit_app
```

7. Run the app:
```bash
streamlit run 00_ℹ️_Info.py
```

The app will be live at ```http://localhost:8501```

---

## 🎬 **Demo**
  
### Stock Predictor Page:
![S&P500 Price Predictor](https://raw.githubusercontent.com/josericodata/SP500Forecaster/main/assets/gifs/sp500forecaster.gif)

---
### ▶️ Watch the YouTube Tutorial


[![Build a Stock Predictor App in 4 Minutes with Streamlit](https://img.youtube.com/vi/aRFjkMZeKhc/maxresdefault.jpg)](https://www.youtube.com/watch?v=aRFjkMZeKhc "Click to play")

Click the image above or [here](https://www.youtube.com/watch?v=aRFjkMZeKhc) to watch the video on YouTube.

---

## 🔮 **Future Enhancements**

Planned improvements and new features include:

- **Integration of advanced ML models** (e.g., LSTM, Prophet) for better prediction accuracy.
- **Multi-stock analysis** to compare performance across different stocks.
- **Sector-based insights** to understand trends within specific industries.
- **User accounts and history tracking** for tailored predictions and personalized experiences.

---

## 🔧 **Environment Setup**

The SP500Forecaster app is built and tested using the following software environment:

- **Operating System**: Ubuntu 22.04.5 LTS (Jammy)
- **Python Version**: Python 3.10.12

Ensure your environment matches or exceeds these versions for optimal performance.

---

## 📋 **Important Notes**

- **Data Requirements**: Stocks with less than two years of historical data will not be processed by the model.
- **Using the Stock Predictor**:
  1. Select a stock ticker from the dropdown menu.
  2. Choose the desired prediction range using the slider.
  3. Click the **Run Prediction** button to generate results.

---

## 🤝 **Open Pull Requests**

If you find any bug, feel free to contact me by opening a pull request on GitHub or via email at **maninastre@gmail.com**.

---

## ⚠️ **Disclaimer**

**This app is designed to demonstrate my skills in data modeling and analytics, showcasing how data-driven insights can assist in building my portfolio as a data analyst. It is not intended to provide financial advice or investment guidance. The predictions are for illustrative purposes only and should not be relied upon for making financial decisions.**
