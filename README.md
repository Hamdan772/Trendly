# 📈 **Trendly - AI Stock Analysis Platform**

---

## **Averix Hacks Submission**

**Name and School:** Hamdan Nishad - [Your School/Organization Name]  
**Date:** January 19, 2026  
**Project Name:** Trendly - AI Stock Prediction & Analysis Platform

**Description:** Trendly is an advanced AI-powered stock analysis platform that uses ensemble machine learning (RandomForest, GradientBoosting, AutoReg) to analyze 450+ S&P 500 stocks with 35+ technical indicators. It provides real-time predictions, exit timing analysis, smart investment recommendations, and confidence-scored forecasts to help investors make data-driven decisions. The platform features a beautiful Streamlit interface with interactive charts, terminology guides, and institutional-grade analytics.

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

2. **Install dependencies**

   **Option A: Using system Python (Quick & Easy)**
   ```bash
   python3 -m pip install -r Trendly/requirements.txt --break-system-packages
   ```

   **Option B: Using virtual environment (Recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r Trendly/requirements.txt
   ```

3. **Run the application**
```bash
cd Trendly
python3 -m streamlit run streamlit_app/00_ℹ️_Info.py --server.port 8505
```

   **Note:** The app is located in the `Trendly/` subfolder within the repository.

4. **Open in browser**
- Navigate to `http://localhost:8505`
- Enter a stock ticker (e.g., AAPL, MSFT, GOOGL, NVDA)
- Click "Analyze Stock" to see AI-powered predictions and insights!

### Troubleshooting

**Import Errors (Pylance warnings in VS Code)?**
- These are just IDE warnings and don't affect functionality
- The app runs perfectly fine with system packages
- To fix: Reload VS Code window (Cmd+Shift+P → "Reload Window")

**Port already in use?**
```bash
# Kill existing Streamlit processes
pkill -9 streamlit
# Then run again
python3 -m streamlit run Trendly/streamlit_app/00_ℹ️_Info.py --server.port 8505
```

**Module not found errors?**
```bash
# Reinstall dependencies
python3 -m pip install -r Trendly/requirements.txt --break-system-packages -q
```

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

## 🌟 **Acknowledgments**

- **Defeat Beta API** for real-time stock data
- **Streamlit** for the amazing web framework
- **scikit-learn** for ML algorithms
- **ta library** for technical analysis indicators
- **S&P 500 dataset** for comprehensive stock coverage

---

<div align="center">

**Made with ❤️ for smarter investing**

⭐ **Star this repo if you found it helpful!** ⭐

[Report Bug](https://github.com/Hamdan772/Trendly/issues) • [Request Feature](https://github.com/Hamdan772/Trendly/issues) • [Documentation](docs/)

</div>
