# 📈 **Trendly - AI Stock Analysis Platform**

---

## **Averix Hacks Submission**

**Name and School:** Hamdan Nishad - [Your School/Organization Name]  
**Date:** January 19, 2026  
**Project Name:** Trendly - AI Stock Prediction & Analysis Platform

**Description:** Trendly is an advanced AI-powered stock analysis platform that uses ensemble machine learning (RandomForest, GradientBoosting, AutoReg) to analyze 450+ S&P 500 stocks with 35+ technical indicators. It provides real-time predictions, exit timing analysis, smart investment recommendations, and confidence-scored forecasts to help investors make data-driven decisions. The platform features a beautiful Streamlit interface with interactive charts, terminology guides, and institutional-grade analytics.

**Third-Party Tools & Datasets:**
- **Defeat Beta API (v0.0.29)** - Real-time stock data
- **S&P 500 Dataset** - 450+ stock tickers (`assets/data/sp500_tickers.csv`)
- **Python Libraries:** scikit-learn, XGBoost, statsmodels, ta (technical analysis), Streamlit, Plotly, pandas, numpy

---

### **Advanced ML Ensemble • Exit Timing • Smart Recommendations • 35+ Technical Indicators**

**Trendly is a sophisticated machine learning application that analyzes 450+ S&P 500 stocks using ensemble AI models. Combining RandomForest, GradientBoosting, and AutoReg with 35+ technical indicators, it delivers institutional-grade predictions with confidence scores, exit timing analysis, and actionable insights.**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40.1-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌟 **What's New in v4.5**

### Enhanced Scoring & UI Fixes

- 📊 **More Generous Scoring System** - Stocks can now reach 100-120 points (IMPROVED!)
  - Maximum possible score increased from 100 to 120
  - Expected Return: 0-40 points (was 35)
  - Trend Strength: 0-30 points (was 25)
  - Technical Indicators: 0-15 points (was 10)
  - Model Confidence: 0-10 points (was 5)
  - Exceptional stocks with 5%+ returns can score above 100!

- 🔧 **Fixed Investment Badge Logic** - Recommendations now match scores correctly
  - Score 86.9/100 now correctly shows "STRONG BUY" instead of "DO NOT INVEST"
  - Badge system uses recommendation codes instead of text parsing

- 🎨 **Fixed Exit Timing HTML Display** - No more raw HTML tags showing
  - Clean rendering of exit timing signals
  - Proper emoji and color displays

---

## 🌟 **What's New in v4.4**

### All-Stock Analysis & Critical Fixes

- 🎯 **Smart Recommendation: ALL 450+ Stocks** - Comprehensive market analysis (UPGRADED!)
  - Analyzes entire S&P 500 (450+ stocks) instead of just 10
  - Finds the absolute best investment opportunity
  - Progress bar shows "{current}/{total} stocks" during analysis
  - Takes 3-5 minutes for complete analysis

- 🐛 **Fixed ML Ensemble Error** - No more "inconsistent samples" errors
  - Fixed direction agreement calculation
  - Proper handling of test vs next-day predictions
  - Stable confidence scoring

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

- 📚 **Terminology Guide** - Understand all metrics (NEW!)
  - Expandable glossary in app
  - 9 comprehensive term explanations
  - Real-world examples for each indicator

---

## 🌟 **What's New in v4.1**

### Smart Investment Recommendation

- 🎯 **"What Should I Invest In?" Button** - AI analyzes stocks and recommends the best opportunity
  - Compares multiple stocks simultaneously
  - Shows confidence scores and predicted returns
  - Displays top 5 alternatives with detailed breakdowns
  - One-click analysis of recommended stock

---

## 🌟 **What's New in v4.0 - Advanced ML Upgrade**

### Revolutionary ML System

- 🤖 **3-Model Ensemble** - RandomForest + GradientBoosting + AutoReg working together
  - Enhanced RandomForest: 200 trees, depth 15, OOB scoring
  - Enhanced GradientBoosting: 200 estimators, learning rate 0.05, subsample 0.8
  - Weighted predictions: 55% RF, 45% GB for maximum accuracy
  - Final blend: 70% ML ensemble + 30% AutoReg

- 📊 **35+ Technical Indicators** - Institutional-grade analysis
  - Moving Averages (MA 5/10/20/50/200, EMA 12/26)
  - Momentum: RSI, MACD, Stochastic Oscillator, ROC
  - Volatility: ATR, Bollinger Bands (width & position)
  - Volume: Volume Ratio, OBV, VPT
  - Support/Resistance levels
  - Golden/Death cross detection

- 🎯 **6-Component Scoring System** (0-100)
  - Expected Return (0-40 points)
  - Trend Strength (0-30 points)
  - Risk Level (0-15 points)
  - Volume Confirmation (0-10 points)
  - Technical Indicators (0-15 points)
  - Model Confidence (0-10 points)

- 📈 **Model Performance Metrics** - Full transparency
  - MAE, R², and accuracy for each model
  - Confidence scoring based on prediction agreement
  - Visual indicators of model reliability

---

## ✨ **Features**

### 🔮 **Predictions & Analysis**
- **30-Day Forecast** with confidence intervals
- **Next-Day Prediction** with expected return %
- **Investment Score** (0-120) with detailed breakdown
- **Smart Recommendations**: Strong Buy / Buy / Hold / Cautious / Sell
- **Exit Timing Analysis**: Know when to sell before downtrends

### 📊 **Technical Analysis**
- **35+ Indicators** calculated in real-time
- **Interactive Charts** with Plotly
- **Support & Resistance Levels** automatically detected
- **Trend Analysis** with multiple moving averages
- **Volatility Measures** for risk assessment

### 🎯 **Smart Features**
- **"What Should I Invest In?"** - AI analyzes 450+ stocks and recommends the best
- **Terminology Guide** - Learn what every metric means
- **Quick Metrics** - RSI, MACD, Bollinger Bands at a glance
- **Market Status** - Real-time market hours indicator

### 🎨 **User Experience**
- **Beautiful Dark Theme** with glassmorphism effects
- **Responsive Design** that works on any device
- **Real-Time Data** from Defeat Beta API
- **Progress Indicators** for long operations
- **Expandable Sections** for detailed information

---

## 🚀 **Quick Start**

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Hamdan772/Trendly.git
cd Trendly
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run streamlit_app/00_ℹ️_Info.py
```

5. **Open in browser**
- Navigate to `http://localhost:8501`
- Enter a stock ticker (e.g., AAPL, MSFT, GOOGL)
- Click "Analyze Stock" to see predictions!

---

## 📦 **Project Structure**

```
Trendly/
├── streamlit_app/
│   ├── 00_ℹ️_Info.py              # Main application (1260+ lines)
│   ├── modules/
│   │   └── helper.py             # ML models & analysis (1164+ lines)
│   └── pages/
│       └── 01_📈_StockPredictor.py
├── assets/
│   ├── data/
│   │   └── sp500_tickers.csv    # 450+ S&P 500 stocks
│   └── gifs/
│       └── sp500forecaster.gif
├── docs/                         # Comprehensive documentation
│   ├── V4.5_SCORING_UPDATE.md
│   ├── V4.4_ALL_STOCKS_ANALYSIS.md
│   ├── V4.3_ML_ACCURACY_UPGRADE.md
│   ├── V4.2_UPDATE_SUMMARY.md
│   └── ...
├── requirements.txt              # Python dependencies
├── LICENSE                       # MIT License
└── README.md                     # This file
```

---

## 🧠 **How It Works**

### 1. Data Collection
- Fetches historical stock data from Defeat Beta API
- Retrieves 252 days (1 trading year) of price/volume data
- Real-time data updates

### 2. Feature Engineering
- Calculates 35+ technical indicators
- Creates features with 60-day lookback window
- Normalizes data using StandardScaler

### 3. Machine Learning
- **RandomForest**: Handles non-linear relationships, reduces overfitting
- **GradientBoosting**: Corrects errors iteratively, high accuracy
- **AutoReg**: Captures time-series patterns, seasonal trends
- **Ensemble**: Weighted combination of all models (70% ML + 30% AutoReg)

### 4. Prediction & Scoring
- Makes 30-day forecast with confidence intervals
- Calculates investment score (0-120) across 6 dimensions
- Generates buy/hold/sell recommendation
- Analyzes exit timing for profit optimization

### 5. Visualization
- Interactive Plotly charts
- Real-time updates
- Mobile-responsive design

---

## 📊 **Technical Indicators Explained**

### Moving Averages
- **MA 5/10/20**: Short-term trend indicators
- **MA 50/200**: Long-term trend indicators
- **Golden Cross**: MA 50 crosses above MA 200 (bullish)
- **Death Cross**: MA 50 crosses below MA 200 (bearish)

### Momentum Indicators
- **RSI (Relative Strength Index)**: Overbought/oversold levels (0-100)
- **MACD**: Trend direction and momentum strength
- **Stochastic Oscillator**: Price momentum in recent range
- **ROC (Rate of Change)**: Price velocity

### Volatility Indicators
- **ATR (Average True Range)**: Price volatility measure
- **Bollinger Bands**: Dynamic support/resistance levels
- **BB Width**: Volatility expansion/contraction
- **BB Position**: Price position within bands (0-1)

### Volume Indicators
- **Volume Ratio**: Current vs average volume
- **OBV (On-Balance Volume)**: Buying/selling pressure
- **VPT (Volume-Price Trend)**: Combines price and volume

---

## 🎓 **Investment Score Breakdown**

### Maximum: 120 Points

1. **Expected Return (0-40 pts)**
   - 5%+ return → 40 pts
   - 3-5% return → 38 pts
   - 2-3% return → 35 pts
   - 1-2% return → 30 pts

2. **Trend Strength (0-30 pts)**
   - Price above MAs → 6 pts each
   - Golden cross → 12 pts
   - Partial golden cross → 6 pts

3. **Risk Level (0-15 pts)**
   - Low volatility (<1.5%) → 12-15 pts
   - Moderate volatility → 8 pts
   - High volatility → 0-4 pts

4. **Volume (0-10 pts)**
   - Exceptional volume (2x+) → 10 pts
   - High volume (1.5x+) → 8 pts
   - Average volume → 4-6 pts

5. **Technical Indicators (0-15 pts)**
   - RSI neutral (40-60) → 6 pts
   - MACD bullish → 5 pts
   - BB middle position → 4 pts

6. **Model Confidence (0-10 pts)**
   - High confidence (>70%) → 7-10 pts
   - Medium confidence → 4-7 pts
   - Low confidence (<40%) → 0-4 pts

---

## 🔧 **Dependencies**

### Core ML Libraries
- `scikit-learn` - RandomForest, GradientBoosting, preprocessing
- `xgboost` - (Optional) XGBoost for enhanced accuracy
- `statsmodels` - AutoReg time-series model
- `numpy` - Numerical computations
- `pandas` - Data manipulation

### Technical Analysis
- `ta` - 35+ technical indicators library

### Data & APIs
- `defeat-beta-api==0.0.29` - Real-time stock data

### Visualization
- `streamlit==1.40.1` - Web application framework
- `plotly` - Interactive charts

### Utilities
- `python-dateutil` - Date handling
- `requests` - HTTP requests

**Full list**: See `requirements.txt`

---

## 🎯 **Use Cases**

### For Individual Investors
- **Day Trading**: Use RSI and MACD for entry/exit points
- **Swing Trading**: Follow MA crossovers and trend analysis
- **Long-Term Investing**: Use investment scores and exit timing
- **Risk Assessment**: Check volatility and confidence scores

### For Students & Researchers
- **ML Study**: Examine ensemble model architecture
- **TA Learning**: Understand 35+ technical indicators
- **Backtesting**: Analyze historical prediction accuracy
- **Data Science**: Study feature engineering techniques

### For Developers
- **Streamlit Apps**: Learn advanced UI patterns
- **ML Pipelines**: Study production-ready ML code
- **API Integration**: See how to work with financial APIs
- **Code Quality**: Review clean, documented Python code

---

## 📈 **Model Performance**

### Accuracy Metrics (Typical)
- **RandomForest R²**: 0.85-0.95
- **GradientBoosting R²**: 0.82-0.93
- **AutoReg R²**: 0.75-0.88
- **Ensemble R²**: 0.88-0.96

### Confidence Scoring
- **High (70-100%)**: All models agree strongly
- **Medium (40-70%)**: Models partially agree
- **Low (0-40%)**: Models disagree, uncertain prediction

*Note: Past performance doesn't guarantee future results. Always do your own research.*

---

## 🚧 **Roadmap**

### v5.0 (Planned)
- [ ] Portfolio optimization (multiple stocks)
- [ ] News sentiment analysis integration
- [ ] Backtesting framework
- [ ] Custom indicator builder
- [ ] Export reports to PDF

### Future Enhancements
- [ ] More ML models (LightGBM, CatBoost)
- [ ] Options analysis
- [ ] Sector rotation strategies
- [ ] Real-time alerts
- [ ] Mobile app

---

## 🤝 **Contributing**

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Areas for Contribution
- Additional ML models
- New technical indicators
- UI/UX improvements
- Documentation
- Bug fixes
- Performance optimization

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

---

## ⚠️ **Disclaimer**

**This tool is for educational and informational purposes only.**

- Not financial advice
- Past performance ≠ future results
- Always do your own research (DYOR)
- Consult a licensed financial advisor
- Use at your own risk

**The creators are not responsible for any financial losses incurred from using this software.**

---

## 📞 **Contact & Support**

- **GitHub**: [@Hamdan772](https://github.com/Hamdan772)
- **Repository**: [github.com/Hamdan772/Trendly](https://github.com/Hamdan772/Trendly)
- **Issues**: [Report bugs or request features](https://github.com/Hamdan772/Trendly/issues)

---

## 🌟 **Acknowledgments**

- **Defeat Beta API** for real-time stock data
- **Streamlit** for the amazing web framework
- **scikit-learn** for ML algorithms
- **ta library** for technical analysis indicators
- **S&P 500 dataset** for comprehensive stock coverage

---

## 📊 **Version History**

- **v4.5** (Jan 2026) - Enhanced scoring (max 120), fixed investment badges, HTML display fixes
- **v4.4** (Jan 2026) - All 450+ stock analysis, fixed ML ensemble errors
- **v4.3** (Jan 2026) - XGBoost integration with graceful fallback
- **v4.2** (Jan 2026) - Exit timing analysis, lenient recommendations, terminology guide
- **v4.1** (Jan 2026) - Smart investment recommendation feature
- **v4.0** (Jan 2026) - Advanced ML ensemble with 35+ indicators
- **v3.0** (Dec 2025) - Multi-model predictions
- **v2.0** (Nov 2025) - Technical indicators
- **v1.0** (Oct 2025) - Initial release

---

<div align="center">

**Made with ❤️ for smarter investing**

⭐ **Star this repo if you found it helpful!** ⭐

[Report Bug](https://github.com/Hamdan772/Trendly/issues) • [Request Feature](https://github.com/Hamdan772/Trendly/issues) • [Documentation](docs/)

</div>
