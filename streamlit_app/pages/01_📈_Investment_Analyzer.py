import streamlit as st
from modules.helper import (fetch_sp_tickers, fetch_stock_history, 
                            generate_investment_analysis)
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Investment Analyzer - Trendly", 
    page_icon="📈", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with better styling
st.markdown("""
<style>
    /* Remove default padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }
    
    /* Score badge with animation */
    .score-badge {
        font-size: 80px;
        font-weight: 900;
        text-align: center;
        padding: 40px;
        border-radius: 25px;
        margin: 30px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        animation: fadeInUp 0.6s ease-out;
        letter-spacing: 2px;
    }
    
    .score-buy {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    }
    
    .score-hold {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
    }
    
    .score-sell {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
    }
    
    /* Recommendation badge */
    .recommendation {
        font-size: 36px;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        font-weight: 800;
        margin: 25px 0;
        animation: fadeInUp 0.8s ease-out;
        letter-spacing: 1px;
    }
    
    .rec-buy {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border: 3px solid #10b981;
    }
    
    .rec-hold {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border: 3px solid #f59e0b;
    }
    
    .rec-sell {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        border: 3px solid #ef4444;
    }
    
    /* Step headers */
    .step-header {
        font-size: 28px;
        font-weight: bold;
        color: #1f2937;
        margin: 30px 0 15px 0;
        padding-left: 10px;
        border-left: 5px solid #3b82f6;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #3b82f6;
        margin: 20px 0;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border: 1px solid #e5e7eb;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Simple divider */
    .divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
        margin: 40px 0;
        border-radius: 10px;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 15px 40px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 12px;
        font-size: 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    /* Success/Info messages */
    .stAlert {
        border-radius: 12px;
        padding: 15px;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 30px;
        border: none;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Sidebar
with st.sidebar:
    st.markdown("## 📊 Control Panel")
    
    # Stock Selection
    st.markdown("### 1️⃣ Select Stock")
    tickers = fetch_sp_tickers()
    ticker_options = [f"{symbol} - {name}" for symbol, name in tickers.items()]
    
    search_term = st.text_input(
        "🔍 Search",
        placeholder="Type symbol or name",
        label_visibility="collapsed"
    )
    
    if search_term:
        filtered_options = [opt for opt in ticker_options if search_term.upper() in opt.upper()]
        ticker_options = filtered_options if filtered_options else ticker_options
    
    selected_option = st.selectbox(
        "Choose company",
        options=ticker_options,
        index=0,
        label_visibility="collapsed"
    )
    
    stock_symbol = selected_option.split(" - ")[0]
    company_name = selected_option.split(" - ")[1]
    
    st.info(f"**{stock_symbol}**  \n{company_name}")
    
    st.markdown("---")
    
    # Forecast Period
    st.markdown("### 2️⃣ Forecast Period")
    days_to_forecast = st.slider(
        "Days to forecast", 
        min_value=7, 
        max_value=90, 
        value=30,
        label_visibility="collapsed"
    )
    st.caption(f"Forecasting **{days_to_forecast} days** ahead")
    
    st.markdown("---")
    
    # Analyze Button
    st.markdown("### 3️⃣ Run Analysis")
    run_analysis = st.button(
        "🚀 Analyze Now", 
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Quick Info
    with st.expander("ℹ️ About Scores"):
        st.markdown("""
        **Score Guide:**
        - 🟢 **70-100**: Strong Buy
        - 🟡 **40-69**: Hold/Monitor
        - 🔴 **0-39**: Avoid/Sell
        
        **Factors:**
        - Return (40%)
        - Trend (30%)
        - Risk (20%)
        - Volume (10%)
        """)
    
    with st.expander("📖 How to Use"):
        st.markdown("""
        1. Search for a stock
        2. Set forecast period
        3. Click "Analyze Now"
        4. Review your score
        5. Make informed decisions
        """)
    
    st.markdown("---")
    st.markdown("**Trendly v2.0**  \n*Smart Investment Analysis*")

# Hero Section
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='font-size: 48px; font-weight: 900; color: #1f2937; margin: 0;'>
        📈 Investment Analyzer
    </h1>
    <p style='font-size: 20px; color: #6b7280; margin-top: 10px;'>
        AI-powered investment analysis for S&P 500 stocks
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Welcome message
st.markdown(f"""
<div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
           padding: 25px; border-radius: 15px; border-left: 5px solid #3b82f6; margin: 20px 0;'>
    <h3 style='color: #1f2937; margin-top: 0;'>📊 Analyzing: {company_name} ({stock_symbol})</h3>
    <p style='color: #4b5563; margin-bottom: 0;'>
        Using the sidebar controls, you've selected to analyze <strong>{stock_symbol}</strong> 
        with a <strong>{days_to_forecast}-day forecast</strong>. Click "Analyze Now" in the sidebar to begin!
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Results Section
if run_analysis:
    with st.spinner('🔄 Analyzing market data and generating predictions... Please wait...'):
        try:
            # Generate analysis
            analysis = generate_investment_analysis(stock_symbol, forecast_days=days_to_forecast)
            
            # Success message
            st.markdown("""
            <div style='background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        border: 2px solid #10b981; margin: 20px 0;'>
                <span style='font-size: 20px; font-weight: bold; color: #065f46;'>
                    ✅ Analysis Complete!
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Results Header
            st.markdown("""
            <div style='text-align: center; padding: 20px 0;'>
                <h2 style='font-size: 36px; font-weight: 800; color: #1f2937; margin: 0;'>
                    📊 Your Investment Report
                </h2>
                <p style='font-size: 18px; color: #6b7280; margin-top: 10px;'>
                    Based on AI analysis and market indicators
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Main Score - Big and Bold
            score = analysis['investment_score']
            decision = analysis['decision']
            
            # Determine color scheme
            if score >= 70:
                score_class = "score-buy"
                rec_class = "rec-buy"
                emoji = "🟢"
                signal = "STRONG BUY"
            elif score >= 40:
                score_class = "score-hold"
                rec_class = "rec-hold"
                emoji = "🟡"
                signal = "HOLD"
            else:
                score_class = "score-sell"
                rec_class = "rec-sell"
                emoji = "🔴"
                signal = "AVOID"
            
            # Score Display with animation
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.markdown(f'''
                <div class="score-badge {score_class}">
                    {emoji}<br>{score}<span style="font-size: 40px;">/100</span>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown(f'''
                <div style='text-align: center; font-size: 28px; font-weight: bold; 
                           color: {"#10b981" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"}; 
                           margin: -10px 0 20px 0; letter-spacing: 3px;'>
                    {signal}
                </div>
                ''', unsafe_allow_html=True)
            
            # Recommendation
            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                st.markdown(f'''
                <div class="recommendation {rec_class}">
                    {decision}
                </div>
                ''', unsafe_allow_html=True)
            
            # Explanation
            st.markdown(f"""
            <div class='info-box'>
                <div style='font-size: 20px; font-weight: bold; color: #1f2937; margin-bottom: 10px;'>
                    💡 What This Means
                </div>
                <div style='font-size: 16px; color: #4b5563; line-height: 1.8;'>
                    {analysis['recommendation']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Key Reasons
            st.markdown("""
            <div style='text-align: center; margin: 30px 0 20px 0;'>
                <h3 style='font-size: 28px; font-weight: 700; color: #1f2937;'>
                    🔍 Why This Score?
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Display reasons as cards
            for i, reason in enumerate(analysis['reasons'], 1):
                st.markdown(f"""
                <div style='background: white; padding: 20px; margin: 15px 0; 
                           border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                           border-left: 5px solid #3b82f6;'>
                    <span style='font-size: 18px; font-weight: 600; color: #3b82f6;'>
                        {i}.
                    </span>
                    <span style='font-size: 16px; color: #4b5563; margin-left: 10px;'>
                        {reason}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Key Metrics in Cards
            st.markdown("""
            <div style='text-align: center; margin: 30px 0 20px 0;'>
                <h3 style='font-size: 28px; font-weight: 700; color: #1f2937;'>
                    📊 Key Metrics
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>💰</div>
                    <div style='font-size: 14px; color: #6b7280; margin-bottom: 5px;'>Current Price</div>
                    <div style='font-size: 24px; font-weight: bold; color: #1f2937;'>${analysis['current_price']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                predicted_change = analysis['predicted_price'] - analysis['current_price']
                change_color = "#10b981" if predicted_change >= 0 else "#ef4444"
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>📈</div>
                    <div style='font-size: 14px; color: #6b7280; margin-bottom: 5px;'>Predicted (Next Day)</div>
                    <div style='font-size: 24px; font-weight: bold; color: {change_color};'>
                        ${analysis['predicted_price']:.2f}
                    </div>
                    <div style='font-size: 14px; color: {change_color}; margin-top: 5px;'>
                        {analysis['predicted_return']:+.2f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                risk_score = analysis['score_breakdown']['Risk Level Score']
                risk_level = "Low" if risk_score >= 15 else ("Medium" if risk_score >= 10 else "High")
                risk_color_text = "#10b981" if risk_score >= 15 else ("#f59e0b" if risk_score >= 10 else "#ef4444")
                risk_emoji = "🟢" if risk_score >= 15 else ("🟡" if risk_score >= 10 else "🔴")
                
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>⚠️</div>
                    <div style='font-size: 14px; color: #6b7280; margin-bottom: 5px;'>Risk Level</div>
                    <div style='font-size: 24px; font-weight: bold; color: {risk_color_text};'>
                        {risk_emoji} {risk_level}
                    </div>
                    <div style='font-size: 14px; color: #6b7280; margin-top: 5px;'>
                        Score: {risk_score}/20
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                trend_score = analysis['score_breakdown']['Trend Strength Score']
                trend_strength = "Strong" if trend_score >= 20 else ("Moderate" if trend_score >= 15 else "Weak")
                trend_color_text = "#10b981" if trend_score >= 20 else ("#f59e0b" if trend_score >= 15 else "#ef4444")
                trend_emoji = "📈" if trend_score >= 20 else ("➡️" if trend_score >= 15 else "📉")
                
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>{trend_emoji}</div>
                    <div style='font-size: 14px; color: #6b7280; margin-bottom: 5px;'>Trend</div>
                    <div style='font-size: 24px; font-weight: bold; color: {trend_color_text};'>
                        {trend_strength}
                    </div>
                    <div style='font-size: 14px; color: #6b7280; margin-top: 5px;'>
                        Score: {trend_score}/30
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Key Numbers - Simple and clear
            st.markdown("## Key Numbers")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Current Price",
                    f"${analysis['current_price']:.2f}"
                )
                st.metric(
                    "Predicted Price (Next Day)",
                    f"${analysis['predicted_price']:.2f}",
                    f"{analysis['predicted_return']:.2f}%"
                )
            
            with col2:
                # Risk level
                risk_score = analysis['score_breakdown']['Risk Level Score']
                risk_level = "Low Risk" if risk_score >= 15 else ("Medium Risk" if risk_score >= 10 else "High Risk")
                risk_color = "�" if risk_score >= 15 else ("🟡" if risk_score >= 10 else "🔴")
                
                st.metric(
                    "Risk Level",
                    f"{risk_color} {risk_level}"
                )
                
                # Trend
                trend_score = analysis['score_breakdown']['Trend Strength Score']
                trend_strength = "Strong Uptrend" if trend_score >= 20 else ("Moderate Trend" if trend_score >= 15 else "Weak/Downtrend")
                trend_color = "🟢" if trend_score >= 20 else ("🟡" if trend_score >= 15 else "🔴")
                
                st.metric(
                    "Trend",
                    f"{trend_color} {trend_strength}"
                )
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Simple price chart
            st.markdown("## Price Forecast")
            st.caption(f"Predicted prices for the next {days_to_forecast} days")
            
            fig = go.Figure()
            
            # Historical (last 90 days)
            fig.add_trace(go.Scatter(
                x=analysis['train_data'].tail(90).index,
                y=analysis['train_data'].tail(90),
                mode='lines',
                name='Historical Price',
                line=dict(color='#3b82f6', width=2)
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=analysis['forecast'].index,
                y=analysis['forecast'],
                mode='lines',
                name='Forecast',
                line=dict(color='#ef4444', width=3, dash='dot')
            ))
            
            fig.update_layout(
                showlegend=True,
                hovermode='x unified',
                template='plotly_white',
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="",
                yaxis_title="Price (USD)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Optional: Show more details
            with st.expander("📊 See Detailed Breakdown"):
                st.markdown("### Score Components")
                
                breakdown = analysis['score_breakdown']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Return Score", f"{breakdown['Expected Return Score']}/40")
                    st.metric("Trend Score", f"{breakdown['Trend Strength Score']}/30")
                
                with col2:
                    st.metric("Risk Score", f"{breakdown['Risk Level Score']}/20")
                    st.metric("Volume Score", f"{breakdown['Volume Confirmation Score']}/10")
                
                st.markdown("### Market Indicators")
                indicators = analysis['latest_indicators']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.text(f"5-Day Avg:  ${indicators['MA_5']:.2f}")
                    st.text(f"10-Day Avg: ${indicators['MA_10']:.2f}")
                    st.text(f"20-Day Avg: ${indicators['MA_20']:.2f}")
                
                with col2:
                    st.text(f"Volatility: {indicators['Volatility']:.2f}%")
                    st.text(f"Volume Ratio: {indicators['Volume_Ratio']:.2f}x")
                    st.text(f"Momentum: {indicators['Momentum']:.2f}%")
            
            # Download option
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Prepare download data
                forecast_df = analysis['forecast'].reset_index()
                forecast_df.columns = ['Date', 'Predicted Price']
                forecast_df['Date'] = forecast_df['Date'].dt.strftime('%Y-%m-%d')
                csv = forecast_df.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download Forecast Data",
                    data=csv,
                    file_name=f"{stock_symbol}_forecast_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please try a different stock or time period.")

else:
    # Instructions before analysis
    st.info("👆 Fill in the details above and click **'Analyze Investment'** to get started")
    
    st.markdown("### What You'll Get:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎯 Clear Score")
        st.markdown("Simple 0-100 rating")
    
    with col2:
        st.markdown("#### 💡 Simple Advice")
        st.markdown("Buy, Hold, or Sell")
    
    with col3:
        st.markdown("#### 📈 Price Forecast")
        st.markdown("Future predictions")

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #999; padding: 20px; font-size: 14px;'>
    <p><strong>⚠️ Educational Tool Only</strong></p>
    <p>Not financial advice. Do your own research.</p>
</div>
""", unsafe_allow_html=True)

