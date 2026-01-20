import streamlit as st
from datetime import datetime, time
from modules.helper import (
    fetch_sp_tickers, 
    fetch_stock_history, 
    generate_investment_analysis,
    get_smart_investment_recommendation
)
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Trendly - AI Stock Analysis", 
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Trendly - AI-powered stock analysis and investment intelligence for educational purposes"
    }
)

# Hide sidebar completely
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Custom CSS with animations and better styling
st.markdown("""
<style>
    /* Global Styles */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    /* Header Styles */
    .app-title {
        font-size: 32px;
        font-weight: 800;
        color: #1f2937;
        letter-spacing: -0.5px;
    }
    
    .header-info {
        text-align: right;
        font-size: 14px;
        color: #6b7280;
        line-height: 1.8;
    }
    
    /* Score Card - Enhanced */
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 45px;
        border-radius: 25px;
        text-align: center;
        color: white;
        box-shadow: 0 25px 70px rgba(102, 126, 234, 0.5);
        margin: 25px 0;
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .score-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }
    
    .score-title {
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 15px;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .score-value {
        font-size: 84px;
        font-weight: 900;
        line-height: 1;
        margin: 15px 0;
        text-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .score-subtitle {
        font-size: 17px;
        margin-top: 15px;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Decision Badge - Enhanced */
    .decision-badge {
        padding: 30px;
        border-radius: 18px;
        text-align: center;
        font-size: 30px;
        font-weight: 800;
        margin: 30px 0;
        letter-spacing: 1px;
        animation: fadeInUp 0.8s ease-out;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .badge-invest {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border: 4px solid #10b981;
    }
    
    .badge-hold {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border: 4px solid #f59e0b;
    }
    
    .badge-avoid {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        border: 4px solid #ef4444;
    }
    
    /* Metric Cards - Enhanced */
    .metric-card {
        background: white;
        padding: 25px 20px;
        border-radius: 15px;
        border: 2px solid #e5e7eb;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .metric-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.25);
        transform: translateY(-5px);
    }
    
    .metric-label {
        font-size: 12px;
        color: #6b7280;
        font-weight: 700;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 22px;
        font-weight: 800;
        color: #1f2937;
    }
    
    /* Input Panel - Enhanced */
    .input-panel {
        background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        animation: fadeInUp 0.4s ease-out;
    }
    
    .panel-title {
        font-size: 24px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Insight Box - Enhanced */
    .insight-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 30px;
        border-radius: 20px;
        border-left: 6px solid #3b82f6;
        margin: 30px 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
        animation: fadeInUp 1s ease-out;
    }
    
    .insight-title {
        font-size: 20px;
        font-weight: 800;
        color: #1e40af;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .insight-text {
        font-size: 16px;
        line-height: 1.8;
        color: #374151;
        font-weight: 400;
    }
    
    /* Section Title - Enhanced */
    .section-title {
        font-size: 26px;
        font-weight: 800;
        color: #1f2937;
        margin: 35px 0 25px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        margin-top: 60px;
        padding: 25px 0;
        border-top: 2px solid #e5e7eb;
        background: linear-gradient(to bottom, transparent, #f9fafb);
    }
    
    /* Button Enhancement */
    .stButton > button {
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Selectbox Enhancement */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 2px solid #e5e7eb !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Placeholder State Enhancement */
    .placeholder-state {
        text-align: center;
        padding: 100px 40px;
        color: #9ca3af;
        animation: fadeInUp 0.5s ease-out;
    }
    
    .placeholder-icon {
        font-size: 80px;
        margin-bottom: 25px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .placeholder-title {
        color: #374151;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .placeholder-text {
        font-size: 17px;
        color: #6b7280;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header Section
st.markdown("""
<div style='text-align: center; padding: 40px 0 30px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin-bottom: 30px; box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);'>
    <h1 style='color: white; font-size: 56px; font-weight: 900; margin-bottom: 10px; text-shadow: 0 4px 10px rgba(0,0,0,0.2); letter-spacing: -1px;'>
        📈 Trendly
    </h1>
    <p style='color: rgba(255,255,255,0.95); font-size: 18px; font-weight: 500; margin-bottom: 25px;'>
        Advanced ML Ensemble • 25+ Technical Indicators • Multi-Model Predictions
    </p>
</div>
""", unsafe_allow_html=True)

# Quick Stats Bar
current_time = datetime.now()
is_weekday = current_time.weekday() < 5
market_open_time = time(9, 30)
market_close_time = time(16, 0)
current_time_only = current_time.time()
is_market_open = is_weekday and market_open_time <= current_time_only <= market_close_time
# Split emoji and text for better rendering
market_emoji = "🟢" if is_market_open else "🔴"
market_text = "OPEN" if is_market_open else "CLOSED"
market_color = "#10b981" if is_market_open else "#ef4444"

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: white; border-radius: 12px; border: 2px solid #e5e7eb;'>
        <div style='font-size: 28px; font-weight: 800; color: {market_color};'>
            <span style='font-size: 32px;'>{market_emoji}</span> {market_text}
        </div>
        <div style='font-size: 12px; color: #6b7280; margin-top: 5px; font-weight: 600;'>Market Status</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: white; border-radius: 12px; border: 2px solid #e5e7eb;'>
        <div style='font-size: 28px; font-weight: 800; color: #667eea;'>450+</div>
        <div style='font-size: 12px; color: #6b7280; margin-top: 5px; font-weight: 600;'>S&P 500 Stocks</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: white; border-radius: 12px; border: 2px solid #e5e7eb;'>
        <div style='font-size: 28px; font-weight: 800; color: #667eea;'>{current_time.strftime('%I:%M')}</div>
        <div style='font-size: 12px; color: #6b7280; margin-top: 5px; font-weight: 600;'>Last Update</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col4:
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: white; border-radius: 12px; border: 2px solid #e5e7eb;'>
        <div style='font-size: 28px; font-weight: 800; color: #667eea;'>AI/ML</div>
        <div style='font-size: 12px; color: #6b7280; margin-top: 5px; font-weight: 600;'>Powered Analysis</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Terminology Glossary Section (Expandable)
with st.expander("📚 **Terminology Guide** - Click to learn what all these metrics mean"):
    st.markdown("""
    <style>
        .term-card {
            background: linear-gradient(135deg, rgba(103, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
            background-color: rgba(0, 0, 0, 0.3);
        }
        .term-title {
            font-size: 18px;
            font-weight: bold;
            color: #8b9dff;
            margin-bottom: 8px;
        }
        .term-description {
            font-size: 14px;
            color: #e0e0e0;
            line-height: 1.6;
        }
        .term-example {
            font-size: 13px;
            color: #b0b0b0;
            font-style: italic;
            margin-top: 5px;
        }
    </style>
    
    <div class="term-card">
        <div class="term-title">🚀 Strong Buy / Buy / Hold / Sell</div>
        <div class="term-description">
            Our AI recommendation based on predicted returns:<br>
            • <strong>Strong Buy (>2%)</strong>: Stock expected to rise significantly<br>
            • <strong>Buy (>0.5%)</strong>: Stock expected to go up<br>
            • <strong>Hold (-0.5% to 0.5%)</strong>: Stock expected to stay flat<br>
            • <strong>Cautious (-1.5% to -0.5%)</strong>: Small expected decline<br>
            • <strong>Sell (<-1.5%)</strong>: Significant expected decline
        </div>
    </div>
    
    <div class="term-card">
        <div class="term-title">📈 RSI (Relative Strength Index)</div>
        <div class="term-description">
            Measures momentum on a scale of 0-100. Shows if a stock is "oversold" or "overbought".<br>
            • <strong>RSI < 30</strong>: Oversold (might bounce back up)<br>
            • <strong>RSI 30-70</strong>: Neutral zone<br>
            • <strong>RSI > 70</strong>: Overbought (might drop soon)
        </div>
        <div class="term-example">Example: RSI of 75 means stock has been rising fast - could be time to take profits</div>
    </div>
    
    <div class="term-card">
        <div class="term-title">〰️ MACD (Moving Average Convergence Divergence)</div>
        <div class="term-description">
            Shows the relationship between two moving averages - helps identify trend changes.<br>
            • <strong>MACD > 0</strong>: Bullish momentum (upward trend)<br>
            • <strong>MACD < 0</strong>: Bearish momentum (downward trend)<br>
            • <strong>MACD crossing up</strong>: Buy signal<br>
            • <strong>MACD crossing down</strong>: Sell signal
        </div>
        <div class="term-example">Example: MACD of -0.50 means downward momentum - price might continue falling</div>
    </div>
    
    <div class="term-card">
        <div class="term-title">📍 Bollinger Bands (BB)</div>
        <div class="term-description">
            Shows volatility boundaries around the price. Like a "normal range" for the stock.<br>
            • <strong>Near Lower Band</strong>: Price is unusually low - might bounce back<br>
            • <strong>Middle Range</strong>: Normal price behavior<br>
            • <strong>Near Upper Band</strong>: Price is unusually high - might pull back
        </div>
        <div class="term-example">Example: "Near Lower BB" means stock is oversold - good buying opportunity</div>
    </div>
    
    <div class="term-card">
        <div class="term-title">📊 ATR (Average True Range)</div>
        <div class="term-description">
            Measures volatility - how much a stock's price typically moves.<br>
            • <strong>High ATR</strong>: Large price swings (risky but potentially high reward)<br>
            • <strong>Low ATR</strong>: Small price movements (stable and safer)
        </div>
        <div class="term-example">Example: ATR of 3.5% means stock typically moves 3.5% per day</div>
    </div>
    
    <div class="term-card">
        <div class="term-title">📦 OBV (On-Balance Volume)</div>
        <div class="term-description">
            Combines price and volume to show buying/selling pressure.<br>
            • <strong>Rising OBV</strong>: More buying pressure - price likely to go up<br>
            • <strong>Falling OBV</strong>: More selling pressure - price likely to go down
        </div>
        <div class="term-example">Example: Rising OBV while price is flat = bullish sign</div>
    </div>
    
    <div class="term-card">
        <div class="term-title">📉 Moving Averages (MA)</div>
        <div class="term-description">
            Average price over a specific period - smooths out daily fluctuations to show trend.<br>
            • <strong>MA 5/10/20</strong>: Short-term trends<br>
            • <strong>MA 50</strong>: Medium-term trend<br>
            • <strong>MA 200</strong>: Long-term trend<br>
            • <strong>Golden Cross</strong>: MA 50 crosses above MA 200 (very bullish)<br>
            • <strong>Death Cross</strong>: MA 50 crosses below MA 200 (very bearish)
        </div>
        <div class="term-example">Example: Price above MA 200 = long-term uptrend</div>
    </div>
    
    <div class="term-card">
        <div class="term-title">🎯 Model Confidence</div>
        <div class="term-description">
            How confident our AI models are in their prediction (0-100%).<br>
            • <strong>> 70%</strong>: High confidence - models agree strongly<br>
            • <strong>40-70%</strong>: Moderate confidence<br>
            • <strong>< 40%</strong>: Low confidence - proceed with caution
        </div>
        <div class="term-example">Example: 85% confidence means all AI models agree on the prediction</div>
    </div>
    
    <div class="term-card">
        <div class="term-title">⏰ Exit Timing</div>
        <div class="term-description">
            Our AI analyzes the forecast to predict when you should sell before a downtrend.<br>
            • <strong>🟢 Safe to Hold</strong>: No exit signal - price rising<br>
            • <strong>🟡 Watch Closely</strong>: Potential peak coming - monitor daily<br>
            • <strong>🔴 Exit Signal</strong>: Sell now or soon - downtrend detected
        </div>
        <div class="term-example">Example: "Exit on Jan 25" means sell before that date to avoid losses</div>
    </div>
    
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Layout
left_col, right_col = st.columns([1, 2])

# INPUT PANEL
with left_col:
    st.markdown('<div class="input-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🔍 Stock Analysis Setup</div>', unsafe_allow_html=True)
    
    # Load S&P 500 tickers
    try:
        sp_tickers = fetch_sp_tickers()
        # Filter out tickers with special characters that may cause API issues
        filtered_tickers = {
            symbol: name for symbol, name in sp_tickers.items() 
            if '.' not in symbol and '-' not in symbol  # Remove tickers like BRK.B, BF.B, etc.
        }
        # Create formatted list: "Company Name (TICKER)"
        ticker_options = [f"{name} ({symbol})" for symbol, name in filtered_tickers.items()]
        ticker_options = sorted(ticker_options)  # Sort alphabetically
        
        # Add count badge
        st.markdown(f"""
        <div style='background: #f0f9ff; padding: 12px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #3b82f6;'>
            <span style='font-size: 14px; color: #1e40af; font-weight: 700;'>📊 {len(ticker_options)} stocks available for analysis</span>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        # Fallback to major stocks if CSV loading fails
        ticker_options = [
            "Apple (AAPL)",
            "Microsoft (MSFT)",
            "NVIDIA (NVDA)",
            "Tesla (TSLA)",
            "Amazon (AMZN)",
            "Alphabet (GOOGL)",
            "Meta Platforms (META)",
            "JPMorgan Chase (JPM)"
        ]
        st.info("📊 Using top 8 major stocks")
    
    # Quick Stock Suggestions
    st.markdown("**💡 Popular Stocks**")
    quick_picks = st.columns(4)
    suggestions = ["AAPL", "MSFT", "NVDA", "TSLA"]
    for i, (col, ticker) in enumerate(zip(quick_picks, suggestions)):
        with col:
            if st.button(ticker, key=f"quick_{ticker}", use_container_width=True):
                # Find the full name for this ticker
                matching = [opt for opt in ticker_options if f"({ticker})" in opt]
                if matching:
                    st.session_state['selected_stock'] = matching[0]
                    st.rerun()
    
    # Smart Investment Recommendation Button
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 3px; border-radius: 8px; margin-bottom: 15px;'>
        <div style='background: white; padding: 2px; border-radius: 6px;'>
    """, unsafe_allow_html=True)
    if st.button("🎯 What Should I Invest In?", key="smart_recommend", use_container_width=True):
        st.session_state['show_recommendation'] = True
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown("<br>**Step 1: Select Stock**", unsafe_allow_html=True)
    
    # Use session state for selected stock if available
    default_index = 0
    if 'selected_stock' in st.session_state:
        try:
            default_index = ticker_options.index(st.session_state['selected_stock'])
        except:
            pass
    
    selected_stock = st.selectbox(
        "Choose a company to analyze",
        options=ticker_options,
        index=default_index,
        help="Select from S&P 500 companies",
        label_visibility="collapsed"
    )
    
    ticker_symbol = selected_stock.split("(")[-1].strip(")")
    
    st.markdown("<br>**Step 2: Historical Data Period**", unsafe_allow_html=True)
    historical_period = st.selectbox(
        "Time period for historical analysis",
        options=["3 months", "6 months", "1 year"],
        index=2,
        help="Longer periods provide more data for analysis",
        label_visibility="collapsed"
    )
    
    period_map = {"3 months": 90, "6 months": 180, "1 year": 365}
    days_back = period_map[historical_period]
    
    st.markdown("<br>**Step 3: Forecast Timeframe**", unsafe_allow_html=True)
    prediction_horizon = st.selectbox(
        "How far ahead to predict",
        options=["Next trading day", "Next 5 trading days"],
        index=0,
        help="Short-term predictions are generally more accurate",
        label_visibility="collapsed"
    )
    
    forecast_days = 1 if prediction_horizon == "Next trading day" else 5
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_clicked = st.button("🚀 Analyze Stock", use_container_width=True)
    
    # Info box
    st.markdown("""
    <div style='margin-top: 20px; padding: 15px; background: #f0f9ff; border-radius: 10px; border-left: 4px solid #3b82f6;'>
        <div style='font-size: 12px; color: #1e40af; font-weight: 600; margin-bottom: 5px;'>🤖 Advanced ML Analysis</div>
        <div style='font-size: 11px; color: #374151; line-height: 1.5;'>
            Our ensemble model combines AutoReg, RandomForest, and GradientBoosting to analyze 25+ technical indicators including RSI, MACD, Bollinger Bands, ATR, and OBV for comprehensive predictions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# RESULTS PANEL
with right_col:
    # Smart Investment Recommendation Display
    if st.session_state.get('show_recommendation', False):
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);'>
            <h2 style='color: white; text-align: center; margin-bottom: 15px; font-size: 32px;'>🎯 AI Investment Recommendation</h2>
            <p style='color: rgba(255,255,255,0.9); text-align: center; font-size: 16px;'>Analyzing 450+ S&P 500 stocks to find the best opportunity... This may take a few minutes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(current, total, ticker):
            progress = current / total
            progress_bar.progress(progress)
            status_text.text(f"Analyzing {ticker}... ({current}/{total} stocks)")
        
        try:
            # Get recommendation - analyze ALL S&P 500 stocks
            recommendation = get_smart_investment_recommendation(
                top_stocks=None,  # This will analyze all 450+ S&P 500 stocks
                progress_callback=update_progress
            )
            
            progress_bar.empty()
            status_text.empty()
            
            if recommendation:
                # Display recommended stock
                ticker = recommendation['recommended_stock']
                company = recommendation['company_name']
                score = recommendation['score']
                confidence = recommendation['confidence']
                pred_return = recommendation['predicted_return']
                
                # Color based on score
                if score >= 70:
                    card_color = "#10b981"
                    emoji = "🚀"
                elif score >= 60:
                    card_color = "#667eea"
                    emoji = "✅"
                else:
                    card_color = "#f59e0b"
                    emoji = "⚠️"
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, {card_color} 0%, {card_color}dd 100%); padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 20px; box-shadow: 0 15px 50px rgba(0,0,0,0.2);'>
                    <div style='font-size: 48px; margin-bottom: 10px;'>{emoji}</div>
                    <h1 style='color: white; font-size: 48px; margin-bottom: 10px; font-weight: 900;'>{ticker}</h1>
                    <h3 style='color: rgba(255,255,255,0.95); font-size: 24px; margin-bottom: 20px;'>{company}</h3>
                    <div style='display: flex; justify-content: center; gap: 40px; margin-top: 30px;'>
                        <div>
                            <div style='color: rgba(255,255,255,0.8); font-size: 14px; margin-bottom: 5px;'>Investment Score</div>
                            <div style='color: white; font-size: 36px; font-weight: 800;'>{score}/100</div>
                        </div>
                        <div>
                            <div style='color: rgba(255,255,255,0.8); font-size: 14px; margin-bottom: 5px;'>Confidence</div>
                            <div style='color: white; font-size: 36px; font-weight: 800;'>{confidence*100:.0f}%</div>
                        </div>
                        <div>
                            <div style='color: rgba(255,255,255,0.8); font-size: 14px; margin-bottom: 5px;'>Predicted Return</div>
                            <div style='color: white; font-size: 36px; font-weight: 800;'>+{pred_return:.2f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Why this stock?
                st.markdown("### 💡 Why This Stock?")
                for reason in recommendation['reasons']:
                    st.markdown(f"• {reason}")
                
                # Show top 5 alternatives
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 📊 Other Top Opportunities")
                
                top_5 = recommendation['all_analyses'][:5]
                for i, stock_data in enumerate(top_5, 1):
                    with st.expander(f"#{i} {stock_data['ticker']} - Score: {stock_data['score']}/100"):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Score", f"{stock_data['score']}/100")
                        col2.metric("Confidence", f"{stock_data['confidence']*100:.0f}%")
                        col3.metric("Return", f"+{stock_data['predicted_return']:.2f}%")
                        st.write("**Top Signals:**")
                        for reason in stock_data['reasons']:
                            st.write(f"• {reason}")
                
                # Analyze this stock button
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"📈 Analyze {ticker} in Detail", use_container_width=True):
                    # Set the stock and clear recommendation
                    matching = [opt for opt in ticker_options if f"({ticker})" in opt]
                    if matching:
                        st.session_state['selected_stock'] = matching[0]
                    st.session_state['show_recommendation'] = False
                    st.rerun()
                
                # Clear button
                if st.button("🔄 Get New Recommendation", use_container_width=True):
                    st.session_state['show_recommendation'] = False
                    st.rerun()
            
            else:
                st.error("❌ Could not generate recommendation. Please try again.")
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error: {str(e)}")
            if st.button("Try Again"):
                st.session_state['show_recommendation'] = False
                st.rerun()
    
    elif analyze_clicked:
        with st.spinner(f"🔄 Analyzing {ticker_symbol}..."):
            try:
                stock_data = fetch_stock_history(ticker_symbol, period="2y")
                
                if stock_data.empty:
                    st.error("❌ No data available for this stock")
                else:
                    cutoff_date = datetime.now() - pd.Timedelta(days=days_back)
                    stock_data_filtered = stock_data[stock_data.index >= cutoff_date]
                    
                    analysis = generate_investment_analysis(ticker_symbol, forecast_days)
                    score = analysis['investment_score']
                    
                    # Score card
                    if score >= 70:
                        score_color = "#667eea"
                        score_subtitle = "Strong trend with controlled risk"
                    elif score >= 50:
                        score_color = "#f59e0b"
                        score_subtitle = "Moderate potential with mixed signals"
                    else:
                        score_color = "#ef4444"
                        score_subtitle = "Weak trend or elevated risk"
                    
                    st.markdown(f"""
                    <div class="score-card" style="background: linear-gradient(135deg, {score_color} 0%, {score_color}dd 100%);">
                        <div class="score-title">Investment Score</div>
                        <div class="score-value">{score} / 100</div>
                        <div class="score-subtitle">{score_subtitle}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Decision badge
                    decision = analysis['decision']
                    recommendation = analysis.get('recommendation', 'HOLD')  # Get the actual recommendation code
                    
                    # Parse recommendation to determine badge style
                    if recommendation in ['STRONG BUY', 'BUY', 'CONSIDER BUY']:
                        if recommendation == 'STRONG BUY':
                            badge_class, badge_icon, badge_text = "badge-invest", "🚀", "STRONG BUY"
                        else:
                            badge_class, badge_icon, badge_text = "badge-invest", "🟢", "YES — INVEST"
                    elif recommendation in ['HOLD', 'CAUTIOUS']:
                        badge_class, badge_icon, badge_text = "badge-hold", "🟡", "HOLD / WATCH"
                    else:  # SELL, AVOID
                        badge_class, badge_icon, badge_text = "badge-avoid", "🔴", "DO NOT INVEST"
                    
                    st.markdown(f"""
                    <div class="decision-badge {badge_class}">
                        {badge_icon} <strong>{badge_text}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Score Breakdown (expandable)
                    with st.expander("📊 View Score Breakdown", expanded=False):
                        breakdown = analysis.get('score_breakdown', {})
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Expected Return", f"{breakdown.get('Expected Return Score', 0)}/40")
                            st.metric("Trend Strength", f"{breakdown.get('Trend Strength Score', 0)}/30")
                        with col2:
                            st.metric("Risk Level", f"{breakdown.get('Risk Level Score', 0)}/20")
                            st.metric("Volume", f"{breakdown.get('Volume Confirmation Score', 0)}/10")
                        
                        st.caption(f"**Predicted Return:** {analysis.get('predicted_return', 0):.2f}%")
                        st.caption(f"**Decision Logic:** Score {score} → {decision}")
                    
                    # Quick Metrics - Derive from available data
                    indicators = analysis.get('latest_indicators', {})
                    
                    # Determine trend based on moving averages and golden cross
                    current_price = analysis.get('current_price', 0)
                    ma_20 = indicators.get('MA_20', 0)
                    ma_50 = indicators.get('MA_50', None)
                    ma_200 = indicators.get('MA_200', None)
                    
                    if ma_50 and ma_200 and ma_50 > ma_200 and current_price > ma_50:
                        trend_value = "Strong Uptrend 🔥"
                    elif current_price > ma_20:
                        trend_value = "Uptrend"
                    elif current_price < ma_20 * 0.98:
                        trend_value = "Downtrend"
                    else:
                        trend_value = "Sideways"
                    
                    # Determine momentum from predicted return
                    predicted_return = analysis.get('predicted_return', 0)
                    if predicted_return > 1:
                        momentum_value = "Positive"
                    elif predicted_return < -1:
                        momentum_value = "Negative"
                    else:
                        momentum_value = "Neutral"
                    
                    # RSI status
                    rsi_14 = indicators.get('RSI_14', None)
                    if rsi_14:
                        if rsi_14 < 30:
                            rsi_value = f"Oversold ({rsi_14:.0f})"
                        elif rsi_14 > 70:
                            rsi_value = f"Overbought ({rsi_14:.0f})"
                        else:
                            rsi_value = f"Neutral ({rsi_14:.0f})"
                    else:
                        rsi_value = "N/A"
                    
                    # MACD status
                    macd_diff = indicators.get('MACD_Diff', None)
                    if macd_diff:
                        if macd_diff > 0:
                            macd_value = "Bullish"
                        else:
                            macd_value = "Bearish"
                    else:
                        macd_value = "N/A"
                    
                    # Determine volatility level
                    volatility = indicators.get('Volatility', 0)
                    if volatility < 1.5:
                        volatility_value = "Low"
                    elif volatility < 3.0:
                        volatility_value = "Medium"
                    else:
                        volatility_value = "High"
                    
                    # Determine volume status
                    volume_ratio = indicators.get('Volume_Ratio', 1.0)
                    if volume_ratio > 1.5:
                        volume_value = "Strong"
                    elif volume_ratio > 1.2:
                        volume_value = "Above Avg"
                    elif volume_ratio < 0.8:
                        volume_value = "Below Avg"
                    else:
                        volume_value = "Average"
                    
                    # Bollinger Bands position
                    bb_position = indicators.get('BB_Position', None)
                    if bb_position:
                        if bb_position < 0.2:
                            bb_value = "Lower Band"
                        elif bb_position > 0.8:
                            bb_value = "Upper Band"
                        else:
                            bb_value = "Middle Range"
                    else:
                        bb_value = "N/A"
                    
                    st.markdown('<div class="section-title">📋 Quick Metrics</div>', unsafe_allow_html=True)
                    metric_cols = st.columns(4)
                    metrics_data = [
                        {"label": "Trend", "value": trend_value, "icon": "📈"},
                        {"label": "Momentum", "value": momentum_value, "icon": "⚡"},
                        {"label": "Volatility", "value": volatility_value, "icon": "📊"},
                        {"label": "Volume", "value": volume_value, "icon": "📦"}
                    ]
                    
                    for col, metric in zip(metric_cols, metrics_data):
                        with col:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div style="font-size: 24px; margin-bottom: 5px;">{metric['icon']}</div>
                                <div class="metric-label">{metric['label']}</div>
                                <div class="metric-value">{metric['value']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Advanced Technical Indicators Row
                    st.markdown('<div class="section-title">🔬 Advanced Indicators</div>', unsafe_allow_html=True)
                    adv_cols = st.columns(4)
                    advanced_metrics = [
                        {"label": "RSI (14)", "value": rsi_value, "icon": "📉"},
                        {"label": "MACD", "value": macd_value, "icon": "〰️"},
                        {"label": "BB Position", "value": bb_value, "icon": "📍"},
                        {"label": "Model Confidence", "value": f"{analysis.get('model_confidence', 0.5)*100:.0f}%", "icon": "🎯"}
                    ]
                    
                    for col, metric in zip(adv_cols, advanced_metrics):
                        with col:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div style="font-size: 24px; margin-bottom: 5px;">{metric['icon']}</div>
                                <div class="metric-label">{metric['label']}</div>
                                <div class="metric-value" style="font-size: 16px;">{metric['value']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Exit Timing Signal Section
                    st.markdown('<div class="section-title">⏰ Exit Timing Analysis</div>', unsafe_allow_html=True)
                    
                    exit_signal = analysis.get('exit_signal', 'HOLD')
                    exit_date = analysis.get('exit_date', None)
                    exit_reason = analysis.get('exit_reason', 'No exit signal detected')
                    exit_confidence = analysis.get('exit_confidence', 0.0)
                    
                    # Determine signal color and emoji
                    if exit_signal == 'EXIT':
                        signal_color = '#ef4444'  # Red
                        signal_emoji = '🔴'
                        signal_label = 'SELL SIGNAL'
                    elif exit_signal == 'WATCH':
                        signal_color = '#f59e0b'  # Orange
                        signal_emoji = '🟡'
                        signal_label = 'WATCH CLOSELY'
                    else:  # HOLD
                        signal_color = '#10b981'  # Green
                        signal_emoji = '🟢'
                        signal_label = 'SAFE TO HOLD'
                    
                    # Build date display
                    date_display = f"📅 {exit_date.strftime('%b %d, %Y')}" if exit_date else ""
                    
                    # Create clean HTML without nested issues
                    exit_html = f"""
                    <div style="background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02)); 
                                border-radius: 15px; padding: 20px; margin: 15px 0;
                                border: 2px solid {signal_color}40;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="font-size: 32px;">{signal_emoji}</div>
                                <div>
                                    <div style="font-size: 24px; font-weight: bold; color: {signal_color};">{signal_label}</div>
                                    <div style="font-size: 14px; color: rgba(255,255,255,0.6);">Confidence: {exit_confidence:.0f}%</div>
                                </div>
                            </div>"""
                    
                    if date_display:
                        exit_html += f"""
                            <div style="font-size: 16px; color: rgba(255,255,255,0.8); background: rgba(255,255,255,0.1); padding: 8px 15px; border-radius: 8px;">{date_display}</div>"""
                    
                    exit_html += f"""
                        </div>
                        <div style="font-size: 16px; color: rgba(255,255,255,0.9); line-height: 1.6;">{exit_reason}</div>
                    </div>
                    """
                    
                    st.markdown(exit_html, unsafe_allow_html=True)
                    
                    # Chart with enhanced styling
                    st.markdown('<div class="section-title">📈 Price & Prediction Chart</div>', unsafe_allow_html=True)
                    
                    fig = go.Figure()
                    
                    # Actual price with enhanced styling
                    fig.add_trace(go.Scatter(
                        x=stock_data_filtered.index, 
                        y=stock_data_filtered['Close'],
                        mode='lines',
                        name='Historical Price',
                        line=dict(color='#3b82f6', width=3),
                        fill='tozeroy',
                        fillcolor='rgba(59, 130, 246, 0.05)',
                        hovertemplate='<b>Date:</b> %{x}<br><b>Price:</b> $%{y:.2f}<extra></extra>'
                    ))
                    
                    if 'forecast' in analysis and len(analysis['forecast']) > 0:
                        forecast_dates = pd.date_range(
                            start=stock_data_filtered.index[-1] + pd.Timedelta(days=1),
                            periods=len(analysis['forecast'])
                        )
                        
                        # Predicted price with enhanced styling
                        fig.add_trace(go.Scatter(
                            x=forecast_dates, 
                            y=analysis['forecast'],
                            mode='lines+markers',
                            name='ML Prediction',
                            line=dict(color='#8b5cf6', width=3, dash='dash'),
                            marker=dict(size=8, symbol='diamond'),
                            hovertemplate='<b>Date:</b> %{x}<br><b>Predicted:</b> $%{y:.2f}<extra></extra>'
                        ))
                    
                
                fig.update_layout(
                    template='plotly_white',
                    hovermode='x unified',
                    height=450,
                    margin=dict(l=10, r=10, t=40, b=10),
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=1.1,
                        xanchor="left",
                        x=0,
                        font=dict(size=13, color='#374151'),
                        bgcolor='rgba(255,255,255,0.8)',
                        bordercolor='#e5e7eb',
                        borderwidth=1
                    ),
                    xaxis=dict(
                        title=dict(
                            text="Date",
                            font=dict(size=14, color='#374151', family='Arial Black')
                        ),
                        showgrid=True,
                        gridcolor='#f3f4f6'
                    ),
                    yaxis=dict(
                        title=dict(
                            text="Price (USD)",
                            font=dict(size=14, color='#374151', family='Arial Black')
                        ),
                        showgrid=True,
                        gridcolor='#f3f4f6'
                    ),
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Model Insight
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown('<div class="insight-title">🧠 Advanced ML Model Insight</div>', unsafe_allow_html=True)
                
                # Model performance indicator
                ml_success = analysis.get('ml_success', False)
                model_confidence = analysis.get('model_confidence', 0.5)
                
                if ml_success:
                    model_info = f"Using ensemble ML (RandomForest + GradientBoosting + AutoReg) with {model_confidence*100:.0f}% confidence. "
                else:
                    model_info = "Using AutoReg time-series model. "
                
                    insight_text = model_info + f"The stock is trading with a {trend_value.lower()} trend"
                
                if momentum_value == "Positive":
                    insight_text += ", showing positive momentum indicators"
                elif momentum_value == "Negative":
                    insight_text += ", with weakening momentum"
                else:
                    insight_text += ", with neutral momentum"
                
                # RSI insight
                if rsi_14:
                    if rsi_14 < 30:
                        insight_text += f". RSI is oversold at {rsi_14:.0f}, suggesting potential bounce opportunity"
                    elif rsi_14 > 70:
                        insight_text += f". RSI is overbought at {rsi_14:.0f}, indicating potential overextension"
                    else:
                        insight_text += f". RSI is in healthy range at {rsi_14:.0f}"
                
                # MACD insight
                if macd_diff:
                    if macd_diff > 0:
                        insight_text += " with bullish MACD momentum"
                    else:
                        insight_text += " while MACD shows bearish momentum"
                
                insight_text += f". Volatility is {volatility_value.lower()}"
                
                if volume_value in ["Strong", "Above Avg"]:
                    insight_text += ", while volume confirms strong investor interest"
                elif volume_value == "Below Avg":
                    insight_text += ", though volume suggests limited participation"
                else:
                    insight_text += ", with typical volume levels"
                
                # Golden Cross mention
                if ma_50 and ma_200 and ma_50 > ma_200:
                    insight_text += ". **Golden Cross detected** (MA50 > MA200), a powerful bullish signal"
                
                if score >= 70:
                    insight_text += ". Based on comprehensive technical analysis, the investment outlook is **strongly favorable**."
                elif score >= 60:
                    insight_text += ". The overall investment outlook is **positive**, suggesting good entry opportunity."
                elif score >= 45:
                    insight_text += ". The investment outlook is **mixed**, suggesting caution and further research."
                else:
                    insight_text += ". Current indicators suggest a **challenging** investment environment."
                
                st.markdown(f'<div class="insight-text">{insight_text}</div>', unsafe_allow_html=True)
                
                # Show model metrics if available
                if ml_success and 'model_metrics' in analysis:
                    metrics = analysis['model_metrics']
                    st.markdown(f"""
                    <div style='margin-top: 12px; padding: 10px; background: rgba(255,255,255,0.5); border-radius: 8px; font-size: 11px;'>
                        <b>Model Performance:</b><br>
                        <div style='display: flex; gap: 15px; margin-top: 5px; flex-wrap: wrap;'>
                            <span>🌲 RF MAE: ${metrics.get('RandomForest_MAE', 0):.2f}</span>
                            <span>📈 GB MAE: ${metrics.get('GradientBoosting_MAE', 0):.2f}</span>
                            <span>🚀 XGB MAE: ${metrics.get('XGBoost_MAE', 0):.2f}</span>
                        </div>
                        <div style='display: flex; gap: 15px; margin-top: 5px; flex-wrap: wrap;'>
                            <span>🌲 RF R²: {metrics.get('RandomForest_R2', 0):.3f}</span>
                            <span>📈 GB R²: {metrics.get('GradientBoosting_R2', 0):.3f}</span>
                            <span>🚀 XGB R²: {metrics.get('XGBoost_R2', 0):.3f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Key Takeaways Summary
                st.markdown('<div class="section-title">🎯 Key Takeaways</div>', unsafe_allow_html=True)
                
                reasons = analysis.get('reasons', [])
                if reasons:
                    takeaway_col1, takeaway_col2 = st.columns(2)
                    with takeaway_col1:
                        st.markdown("""
                        <div style='background: #f0fdf4; padding: 20px; border-radius: 12px; border-left: 4px solid #10b981;'>
                            <h4 style='color: #065f46; margin-bottom: 10px;'>✅ Positive Signals</h4>
                        """, unsafe_allow_html=True)
                        for reason in reasons[:3]:
                            st.markdown(f"• {reason}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with takeaway_col2:
                        st.markdown("""
                        <div style='background: #fef3c7; padding: 20px; border-radius: 12px; border-left: 4px solid #f59e0b;'>
                        <h4 style='color: #92400e; margin-bottom: 10px;'>⚠️ Considerations</h4>
                        <p style='color: #78350f; margin: 5px 0;'>• Past performance doesn't guarantee future results</p>
                        <p style='color: #78350f; margin: 5px 0;'>• Market conditions can change rapidly</p>
                        <p style='color: #78350f; margin: 5px 0;'>• Consider your risk tolerance and goals</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            except Exception as e:
                error_message = str(e)
                st.error(f"❌ Error analyzing stock: {error_message}")
                # Provide helpful guidance based on error type
                if "No data found" in error_message or "ticker" in error_message.lower():
                    st.warning("""
                    **📋 Stock Not Available**
                    
                    This stock may not be available in our data provider. Common reasons:
                    - Special characters in ticker (e.g., BRK.B) may not be supported
                    - Stock may be delisted or unavailable
                    - Data provider may not cover this security
                    
                    **Try these popular stocks instead:**
                    - Apple (AAPL)
                    - Microsoft (MSFT)
                    - NVIDIA (NVDA)
                    - Tesla (TSLA)
                    - Amazon (AMZN)
                    """)
                else:
                    st.info("💡 Please try another stock or refresh the page.")
    else:
        # Enhanced Placeholder state
        st.markdown("""
        <div class='placeholder-state'>
            <div class='placeholder-icon'>📊</div>
            <h2 class='placeholder-title'>Ready to Analyze Stocks</h2>
            <p class='placeholder-text'>
                Select a stock from the panel on the left, choose your analysis parameters,<br>
                and click <strong>"Analyze Stock"</strong> to get comprehensive ML-powered insights
            </p>
            <br>
            <div style='display: flex; justify-content: center; gap: 40px; margin-top: 30px;'>
                <div style='text-align: center;'>
                    <div style='font-size: 36px; color: #667eea;'>🎯</div>
                    <div style='font-size: 14px; color: #6b7280; margin-top: 10px;'>Investment Score</div>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 36px; color: #667eea;'>📈</div>
                    <div style='font-size: 14px; color: #6b7280; margin-top: 10px;'>Price Forecast</div>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 36px; color: #667eea;'>🧠</div>
                    <div style='font-size: 14px; color: #6b7280; margin-top: 10px;'>AI Insights</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Enhanced Footer with Features
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

# Feature Highlights
feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 15px;'>
        <div style='font-size: 36px; margin-bottom: 10px;'>🤖</div>
        <h4 style='color: #1e40af; margin-bottom: 10px;'>Ensemble ML</h4>
        <p style='color: #6b7280; font-size: 14px;'>RandomForest + GradientBoosting + AutoReg</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-radius: 15px;'>
        <div style='font-size: 36px; margin-bottom: 10px;'>📊</div>
        <h4 style='color: #065f46; margin-bottom: 10px;'>25+ Indicators</h4>
        <p style='color: #6b7280; font-size: 14px;'>RSI, MACD, Bollinger Bands, ATR, OBV & more</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 15px;'>
        <div style='font-size: 36px; margin-bottom: 10px;'>🎯</div>
        <h4 style='color: #92400e; margin-bottom: 10px;'>High Confidence</h4>
        <p style='color: #6b7280; font-size: 14px;'>Multi-model consensus with confidence scores</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 20px; box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);'>
    <h2 style='color: white; font-size: 32px; font-weight: 800; margin-bottom: 15px;'>⚠️ Important Disclaimer</h2>
    <p style='color: rgba(255,255,255,0.95); font-size: 16px; line-height: 1.8; max-width: 800px; margin: 0 auto;'>
        This application is for <strong>educational purposes only</strong> and does not constitute financial advice.
        Past performance does not guarantee future results. Stock markets are inherently risky.
        Always conduct thorough research and consult with qualified financial advisors before making investment decisions.
    </p>
    <div style='margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);'>
        <p style='color: rgba(255,255,255,0.9); font-size: 14px;'>
            © 2026 Trendly | Powered by Machine Learning & Real-Time Market Data<br>
            <span style='font-size: 12px; color: rgba(255,255,255,0.7);'>Built with Streamlit, Plotly, and Advanced AI Models</span>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
