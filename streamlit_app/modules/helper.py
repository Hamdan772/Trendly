import pandas as pd
import numpy as np
import streamlit as st
from statsmodels.tsa.ar_model import AutoReg
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, r2_score

# Try to import XGBoost, fallback gracefully if not available
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except (ImportError, Exception) as e:
    XGBOOST_AVAILABLE = False
    print(f"XGBoost not available: {e}")
    print("Continuing with RandomForest and GradientBoosting only")

from defeatbeta_api.data.ticker import Ticker
import ta  # Technical Analysis library
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

@st.cache_data
def fetch_sp_tickers():
    """Fetch the S&P tickers from the CSV file in the assets folder."""
    try:
      
        # Read the CSV file
        df = pd.read_csv("../assets/data/sp500_tickers.csv")
        
        # Convert to a dictionary
        sp_tickers = df.set_index("Symbol")["Security"].to_dict()
        return sp_tickers
    
    except FileNotFoundError as fnfe:
        raise Exception(str(fnfe))
    except Exception as e:
        raise Exception(f"An error occurred while fetching tickers: {e}")



def fetch_stock_history(stock_ticker, period="max", interval="1d"):
    """
    Fetch historical stock data from Defeat Beta API with Volume included.
    Args:
        stock_ticker (str): The stock ticker symbol.
        period (str): The time period for the data ('max', '2y', etc.).
        interval (str): The interval for the data (only '1d' supported).
    Returns:
        pd.DataFrame: A DataFrame containing stock data with columns ['Open', 'High', 'Low', 'Close', 'Volume'].
    """
    try:
        # Initialize Defeat Beta Ticker
        ticker = Ticker(stock_ticker)
        
        # Fetch price data (automatically gets full historical data)
        data = ticker.price()
        
        if data.empty:
            raise ValueError(f"No data found for ticker {stock_ticker}.")
        
        # Rename columns to match expected format
        data = data.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume',
            'report_date': 'Date'
        })
        
        # Set Date as index
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])
            data = data.set_index('Date')
        
        # Sort by date (ascending)
        data = data.sort_index()
        
        # Filter based on period
        if period == "2y":
            two_years_ago = datetime.now() - timedelta(days=730)
            data = data[data.index >= two_years_ago]
        
        return data[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    except ValueError as ve:
        raise ValueError(str(ve))
    except Exception as e:
        raise Exception(f"Error fetching stock data for {stock_ticker}: {e}")


def engineer_features(stock_data):
    """
    Engineer comprehensive advanced features for investment decision-making.
    
    Features include:
    1. Past Prices (Memory of the Market)
    2. Moving Averages (Trend Detection) - SMA & EMA
    3. Momentum Indicators - RSI, MACD, Stochastic
    4. Volatility Measures - ATR, Bollinger Bands
    5. Volume Indicators - OBV, Volume Oscillator
    6. Pattern Recognition - Support/Resistance levels
    
    Args:
        stock_data (pd.DataFrame): Historical stock data with OHLCV columns
    Returns:
        pd.DataFrame: Enhanced dataframe with advanced engineered features
    """
    df = stock_data.copy()
    
    # 1. PAST PRICES (Memory of the Market)
    df['Prev_Close_1'] = df['Close'].shift(1)
    df['Prev_Close_2'] = df['Close'].shift(2)
    df['Prev_Close_5'] = df['Close'].shift(5)
    
    # 2. MOVING AVERAGES (Trend Detection) - Both SMA and EMA
    # Simple Moving Averages
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['MA_10'] = df['Close'].rolling(window=10).mean()
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    df['MA_200'] = df['Close'].rolling(window=200).mean()
    
    # Exponential Moving Averages (more weight to recent data)
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    
    # MA Crossovers (Strong buy/sell signals)
    df['MA_5_10_Cross'] = (df['MA_5'] > df['MA_10']).astype(int)
    df['MA_50_200_Cross'] = (df['MA_50'] > df['MA_200']).astype(int)  # Golden Cross
    
    # 3. MOMENTUM INDICATORS
    df['Price_Change'] = df['Close'].diff()
    df['Daily_Return'] = df['Close'].pct_change() * 100
    
    # RSI (Relative Strength Index) - Overbought/Oversold indicator
    df['RSI_14'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    
    # MACD (Moving Average Convergence Divergence)
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Diff'] = macd.macd_diff()
    
    # Stochastic Oscillator
    stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'])
    df['Stoch_K'] = stoch.stoch()
    df['Stoch_D'] = stoch.stoch_signal()
    
    # Rate of Change (ROC)
    df['ROC_10'] = ((df['Close'] - df['Close'].shift(10)) / df['Close'].shift(10)) * 100
    
    # 4. VOLATILITY MEASURES (Risk Awareness)
    df['High_Low_Range'] = df['High'] - df['Low']
    df['Volatility_5'] = df['Daily_Return'].rolling(window=5).std()
    df['Volatility_10'] = df['Daily_Return'].rolling(window=10).std()
    df['Volatility_20'] = df['Daily_Return'].rolling(window=20).std()
    
    # ATR (Average True Range) - Better volatility measure
    df['ATR_14'] = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close'], window=14).average_true_range()
    
    # Bollinger Bands
    bollinger = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
    df['BB_High'] = bollinger.bollinger_hband()
    df['BB_Mid'] = bollinger.bollinger_mavg()
    df['BB_Low'] = bollinger.bollinger_lband()
    df['BB_Width'] = df['BB_High'] - df['BB_Low']
    df['BB_Position'] = (df['Close'] - df['BB_Low']) / (df['BB_High'] - df['BB_Low'])
    
    # 5. VOLUME INDICATORS (Market Confidence)
    df['Avg_Volume_10'] = df['Volume'].rolling(window=10).mean()
    df['Avg_Volume_20'] = df['Volume'].rolling(window=20).mean()
    df['Volume_Ratio'] = df['Volume'] / df['Avg_Volume_10']
    
    # On-Balance Volume (OBV)
    df['OBV'] = ta.volume.OnBalanceVolumeIndicator(df['Close'], df['Volume']).on_balance_volume()
    
    # Volume Price Trend
    df['VPT'] = ta.volume.VolumePriceTrendIndicator(df['Close'], df['Volume']).volume_price_trend()
    
    # 6. PATTERN RECOGNITION
    # Support and Resistance levels (20-day min/max)
    df['Support_20'] = df['Low'].rolling(window=20).min()
    df['Resistance_20'] = df['High'].rolling(window=20).max()
    df['Distance_Support'] = ((df['Close'] - df['Support_20']) / df['Support_20']) * 100
    df['Distance_Resistance'] = ((df['Resistance_20'] - df['Close']) / df['Close']) * 100
    
    # Price position indicators
    df['Price_Above_MA5'] = (df['Close'] > df['MA_5']).astype(int)
    df['Price_Above_MA10'] = (df['Close'] > df['MA_10']).astype(int)
    df['Price_Above_MA20'] = (df['Close'] > df['MA_20']).astype(int)
    df['Price_Above_MA50'] = (df['Close'] > df['MA_50']).astype(int)
    df['Price_Above_MA200'] = (df['Close'] > df['MA_200']).astype(int)
    
    return df


def calculate_exit_timing(forecast, current_price, indicators):
    """
    Analyze forecast to determine optimal exit point before downtrend.
    
    Args:
        forecast (pd.Series): Future price predictions
        current_price (float): Current stock price
        indicators (dict): Latest technical indicators
    
    Returns:
        dict: {
            'signal': str ('HOLD' | 'WATCH' | 'EXIT'),
            'date': datetime | None,
            'reason': str,
            'confidence': float (0-100)
        }
    """
    try:
        if forecast is None or len(forecast) == 0:
            return {
                'signal': 'HOLD',
                'date': None,
                'reason': 'Insufficient data for exit analysis',
                'confidence': 0.0
            }
        
        # Convert forecast to numpy array for easier manipulation
        forecast_vals = forecast.values if hasattr(forecast, 'values') else np.array(forecast)
        forecast_dates = forecast.index if hasattr(forecast, 'index') else None
        
        # Find peak in forecast
        peak_idx = np.argmax(forecast_vals)
        peak_price = forecast_vals[peak_idx]
        peak_date = forecast_dates[peak_idx] if forecast_dates is not None else None
        
        # Check if we're already past peak
        if peak_idx <= 1:
            # Peak is at start or very soon
            confidence_factors = []
            
            # Check technical indicators for bearish signals
            rsi = indicators.get('RSI_14', 50)
            macd = indicators.get('MACD_Diff', 0)
            bb_position = indicators.get('BB_Position', 0.5)
            
            # RSI overbought?
            if rsi > 70:
                confidence_factors.append(25)  # Strong signal
            elif rsi > 60:
                confidence_factors.append(15)  # Moderate signal
            
            # MACD bearish?
            if macd < 0:
                confidence_factors.append(20)
            
            # Bollinger Band position?
            if bb_position > 0.8:
                confidence_factors.append(25)  # Near upper band
            
            # Calculate confidence
            confidence = sum(confidence_factors)
            
            if confidence >= 50:
                return {
                    'signal': 'EXIT',
                    'date': peak_date,
                    'reason': f'Peak detected - price may decline from ${peak_price:.2f}',
                    'confidence': min(confidence, 95.0)
                }
            elif confidence >= 30:
                return {
                    'signal': 'WATCH',
                    'date': peak_date,
                    'reason': f'Near potential peak at ${peak_price:.2f} - monitor closely',
                    'confidence': confidence
                }
        
        # Look for sustained decline after peak
        if peak_idx < len(forecast_vals) - 2:
            # Check for consecutive declines after peak
            post_peak = forecast_vals[peak_idx + 1:]
            decline_count = 0
            for i in range(len(post_peak) - 1):
                if post_peak[i] > post_peak[i + 1]:
                    decline_count += 1
                else:
                    break
            
            # Calculate total decline from peak
            if len(post_peak) > 0:
                final_price = post_peak[-1]
                decline_pct = ((peak_price - final_price) / peak_price) * 100
                
                # Significant decline detected?
                if decline_count >= 2 and decline_pct > 2.0:
                    # Recommend exit 1 day before peak
                    exit_idx = max(0, peak_idx - 1)
                    exit_date = forecast_dates[exit_idx] if forecast_dates is not None else None
                    exit_price = forecast_vals[exit_idx]
                    
                    # Calculate confidence based on decline strength
                    confidence = min(50 + (decline_pct * 5) + (decline_count * 10), 95.0)
                    
                    return {
                        'signal': 'EXIT',
                        'date': exit_date,
                        'reason': f'Sell before peak at ${exit_price:.2f} (expected {decline_pct:.1f}% decline)',
                        'confidence': confidence
                    }
                elif decline_count >= 1 and decline_pct > 1.0:
                    # Moderate decline - watch signal
                    confidence = 40 + (decline_pct * 3)
                    return {
                        'signal': 'WATCH',
                        'date': peak_date,
                        'reason': f'Potential peak at ${peak_price:.2f} - consider taking profits',
                        'confidence': confidence
                    }
        
        # Check if price is rising steadily (good time to hold)
        if peak_idx >= len(forecast_vals) - 2:
            # Peak is at or near end - price rising
            gain_from_current = ((peak_price - current_price) / current_price) * 100
            
            if gain_from_current > 3.0:
                return {
                    'signal': 'HOLD',
                    'date': None,
                    'reason': f'Price rising to ${peak_price:.2f} (+{gain_from_current:.1f}%) - hold position',
                    'confidence': 70.0
                }
            elif gain_from_current > 1.0:
                return {
                    'signal': 'HOLD',
                    'date': None,
                    'reason': f'Moderate uptrend to ${peak_price:.2f} (+{gain_from_current:.1f}%)',
                    'confidence': 60.0
                }
        
        # Default: hold position
        return {
            'signal': 'HOLD',
            'date': None,
            'reason': 'No clear exit signal - maintain position',
            'confidence': 50.0
        }
        
    except Exception as e:
        return {
            'signal': 'HOLD',
            'date': None,
            'reason': f'Exit analysis unavailable',
            'confidence': 0.0
        }


def calculate_investment_score(predicted_return, current_price, ma_5, ma_10, ma_20, 
                                volatility, volume_ratio, rsi=None, macd_diff=None, bb_position=None,
                                ma_50=None, ma_200=None, model_confidence=None):
    """
    Calculate comprehensive investment score (0-100) based on multiple advanced factors.
    
    Scoring Breakdown:
    - Expected Return (0-35 points): Rewards profit potential
    - Trend Strength (0-25 points): Evaluates price position vs moving averages
    - Risk Level (0-15 points): Considers volatility
    - Volume Confirmation (0-10 points): Checks market participation
    - Technical Indicators (0-10 points): RSI, MACD, Bollinger Bands
    - Model Confidence (0-5 points): Prediction reliability
    
    Args:
        predicted_return (float): Expected return percentage
        current_price (float): Current stock price
        ma_5, ma_10, ma_20 (float): Moving averages
        volatility (float): Stock volatility measure
        volume_ratio (float): Current volume vs average volume
        rsi (float, optional): Relative Strength Index
        macd_diff (float, optional): MACD histogram value
        bb_position (float, optional): Position within Bollinger Bands (0-1)
        ma_50, ma_200 (float, optional): Long-term moving averages
        model_confidence (float, optional): Model prediction confidence (0-1)
    
    Returns:
        tuple: (total_score, breakdown_dict)
    """
    
    # 1️⃣ EXPECTED RETURN SCORE (0-35 points) - More realistic
    if predicted_return >= 3.0:
        return_score = 35  # 3%+ return = excellent
    elif predicted_return >= 2.0:
        return_score = 30  # 2-3% return = very good
    elif predicted_return >= 1.0:
        return_score = 25  # 1-2% return = good
    elif predicted_return >= 0.5:
        return_score = 18  # 0.5-1% return = decent
    elif predicted_return > 0:
        return_score = 10  # Small positive = okay
    elif predicted_return > -0.5:
        return_score = 5   # Slight negative = risky
    elif predicted_return > -1.0:
        return_score = 2   # Moderate negative = very risky
    else:
        return_score = 0   # Large negative = avoid
    
    # 2️⃣ TREND STRENGTH SCORE (0-25 points)
    trend_score = 0
    if current_price > ma_5:
        trend_score += 5   # Above short-term MA
    if current_price > ma_10:
        trend_score += 5   # Above medium-term MA
    if current_price > ma_20:
        trend_score += 5   # Above longer-term MA
    
    # Golden Cross / Death Cross (powerful signal)
    if ma_50 is not None and ma_200 is not None:
        if ma_50 > ma_200 and current_price > ma_50:
            trend_score += 10  # Golden cross + price above = strong uptrend
        elif ma_50 < ma_200:
            trend_score -= 5   # Death cross = penalty
    
    trend_score = max(0, trend_score)  # Don't go negative
    
    # 3️⃣ RISK LEVEL SCORE (0-15 points)
    if volatility < 1.0:
        risk_score = 15  # Very low volatility = very safe
    elif volatility < 1.5:
        risk_score = 12  # Low volatility = safe
    elif volatility < 2.5:
        risk_score = 8   # Moderate volatility = acceptable
    elif volatility < 4.0:
        risk_score = 4   # High volatility = risky
    else:
        risk_score = 0   # Very high volatility = very risky
    
    # 4️⃣ VOLUME CONFIRMATION SCORE (0-10 points)
    if volume_ratio > 2.0:
        volume_score = 10  # Exceptional volume
    elif volume_ratio > 1.5:
        volume_score = 8   # Very high volume
    elif volume_ratio > 1.2:
        volume_score = 6   # Above average volume
    elif volume_ratio > 1.0:
        volume_score = 4   # Average volume
    elif volume_ratio > 0.8:
        volume_score = 2   # Below average volume
    else:
        volume_score = 0   # Low volume = no conviction
    
    # 5️⃣ TECHNICAL INDICATORS SCORE (0-10 points)
    technical_score = 0
    
    # RSI Analysis (0-4 points)
    if rsi is not None:
        if 40 <= rsi <= 60:
            technical_score += 4  # Neutral zone = healthy
        elif 30 <= rsi < 40 or 60 < rsi <= 70:
            technical_score += 3  # Slightly oversold/overbought
        elif 20 <= rsi < 30 or 70 < rsi <= 80:
            technical_score += 1  # Oversold/overbought warning
        # RSI < 20 or > 80 = 0 points (extreme)
    
    # MACD Analysis (0-3 points)
    if macd_diff is not None:
        if macd_diff > 0:
            technical_score += 3  # Bullish momentum
        elif macd_diff > -0.5:
            technical_score += 1  # Weak bearish
    
    # Bollinger Bands Position (0-3 points)
    if bb_position is not None:
        if 0.3 <= bb_position <= 0.7:
            technical_score += 3  # Middle of bands = healthy
        elif 0.1 <= bb_position < 0.3 or 0.7 < bb_position <= 0.9:
            technical_score += 2  # Near edges
        elif bb_position < 0.1:
            technical_score += 1  # Oversold area (potential bounce)
    
    # 6️⃣ MODEL CONFIDENCE SCORE (0-5 points)
    confidence_score = 0
    if model_confidence is not None:
        confidence_score = model_confidence * 5  # Scale 0-1 to 0-5
    
    # CALCULATE TOTAL SCORE
    total_score = return_score + trend_score + risk_score + volume_score + technical_score + confidence_score
    
    # Create detailed breakdown dictionary
    breakdown = {
        'Expected Return Score': round(return_score, 1),
        'Trend Strength Score': round(trend_score, 1),
        'Risk Level Score': round(risk_score, 1),
        'Volume Confirmation Score': round(volume_score, 1),
        'Technical Indicators Score': round(technical_score, 1),
        'Model Confidence Score': round(confidence_score, 1),
        'Total Score': round(total_score, 1)
    }
    
    return round(total_score, 1), breakdown


def get_investment_recommendation(score, predicted_return=None):
    """
    Convert investment score to clear recommendation with focus on predicted returns.
    More lenient approach - if it's going up, consider buying.
    
    Args:
        score (float): Investment score (0-100)
        predicted_return (float, optional): Predicted return percentage
    
    Returns:
        tuple: (decision, recommendation, color)
    """
    # If predicted return is positive and score is reasonable, lean towards buy
    if predicted_return is not None and predicted_return > 0:
        if score >= 55:  # Lowered from 60
            if score >= 70:
                return "🚀 Strong Buy", "STRONG BUY", "green"
            return "✅ Buy", "BUY", "green"
        elif score >= 40:  # Lowered from 45
            return "📈 Consider Buying", "CONSIDER BUY", "green"
        elif score >= 30:  # Even slight positives get consideration
            return "⚠️ Hold / Watch", "HOLD", "orange"
        else:
            return "⚡ High Risk", "CAUTIOUS", "orange"
    else:
        # Negative or flat predictions
        if score >= 70:
            return "✅ Buy", "BUY", "green"
        elif score >= 50:
            return "⚠️ Hold", "HOLD", "orange"
        elif score >= 30:
            return "⚡ Cautious", "CAUTIOUS", "orange"
        else:
            return "❌ Avoid", "SELL", "red"


def prepare_ml_features(df, lookback=60):
    """
    Prepare features for machine learning models with proper lookback window.
    
    Args:
        df (pd.DataFrame): Enhanced dataframe with engineered features
        lookback (int): Number of days to look back for features
    
    Returns:
        tuple: (X, y, feature_names) - Features, targets, and feature names
    """
    # Select relevant features for ML models
    feature_columns = [
        'MA_5', 'MA_10', 'MA_20', 'MA_50', 'MA_200',
        'EMA_12', 'EMA_26',
        'RSI_14', 'MACD', 'MACD_Signal', 'MACD_Diff',
        'Stoch_K', 'Stoch_D', 'ROC_10',
        'Volatility_10', 'Volatility_20', 'ATR_14',
        'BB_Position', 'BB_Width',
        'Volume_Ratio', 'OBV', 'VPT',
        'Distance_Support', 'Distance_Resistance',
        'MA_5_10_Cross', 'MA_50_200_Cross'
    ]
    
    # Create target: Next day's return
    df['Target'] = df['Close'].shift(-1)
    
    # Remove rows with NaN values
    df_clean = df[feature_columns + ['Target', 'Close']].dropna()
    
    if len(df_clean) < lookback:
        raise ValueError(f"Not enough data after feature engineering. Need at least {lookback} days.")
    
    X = df_clean[feature_columns].values
    y = df_clean['Target'].values
    
    return X, y, feature_columns, df_clean['Close'].values


def train_ensemble_models(X_train, y_train):
    """
    Train ensemble of ML models for better prediction accuracy.
    
    Args:
        X_train: Training features
        y_train: Training targets
    
    Returns:
        dict: Dictionary of trained models with their names
    """
    models = {}
    
    # 1. Random Forest - Handles non-linear patterns well (ENHANCED)
    rf_model = RandomForestRegressor(
        n_estimators=200,  # Increased from 100
        max_depth=15,  # Increased from 10
        min_samples_split=3,  # Reduced from 5 for better learning
        min_samples_leaf=1,  # Reduced from 2 for finer patterns
        max_features='sqrt',  # Better feature selection
        random_state=42,
        n_jobs=-1,
        bootstrap=True,
        oob_score=True  # Out-of-bag score for validation
    )
    rf_model.fit(X_train, y_train)
    models['RandomForest'] = rf_model
    
    # 2. Gradient Boosting - Sequential error correction (ENHANCED)
    gb_model = GradientBoostingRegressor(
        n_estimators=200,  # Increased from 100
        max_depth=6,  # Increased from 5
        learning_rate=0.05,  # Reduced for better convergence
        min_samples_split=3,  # Reduced from 5
        min_samples_leaf=1,  # Reduced from 2
        subsample=0.8,  # Add subsample for regularization
        max_features='sqrt',  # Better feature selection
        random_state=42
    )
    gb_model.fit(X_train, y_train)
    models['GradientBoosting'] = gb_model
    
    # 3. XGBoost - State-of-the-art gradient boosting (if available)
    if XGBOOST_AVAILABLE:
        try:
            xgb_model = xgb.XGBRegressor(
                n_estimators=200,
                max_depth=7,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                gamma=0.1,  # Minimum loss reduction
                reg_alpha=0.1,  # L1 regularization
                reg_lambda=1.0,  # L2 regularization
                min_child_weight=1,
                random_state=42,
                n_jobs=-1,
                tree_method='hist',  # Faster training
                early_stopping_rounds=10
            )
            
            # Split training data for early stopping
            split_idx = int(len(X_train) * 0.9)
            X_train_fit = X_train[:split_idx]
            y_train_fit = y_train[:split_idx]
            X_val = X_train[split_idx:]
            y_val = y_train[split_idx:]
            
            xgb_model.fit(
                X_train_fit, y_train_fit,
                eval_set=[(X_val, y_val)],
                verbose=False
            )
            models['XGBoost'] = xgb_model
        except Exception as e:
            print(f"XGBoost model training failed: {e}")
            print("Continuing with RandomForest and GradientBoosting")
    
    return models


def ensemble_predict(models, X_test, weights=None):
    """
    Make ensemble predictions by combining multiple models with optimized weighting.
    
    Args:
        models (dict): Dictionary of trained models
        X_test: Test features
        weights (dict, optional): Weights for each model
    
    Returns:
        tuple: (ensemble_prediction, individual_predictions, confidence)
    """
    if weights is None:
        # Optimized weights based on typical model performance
        if 'XGBoost' in models:
            # XGBoost typically performs best, so give it highest weight
            weights = {
                'XGBoost': 0.45,  # Highest weight
                'RandomForest': 0.30,
                'GradientBoosting': 0.25
            }
        else:
            # If XGBoost not available, use equal weights for RF and GB
            weights = {
                'RandomForest': 0.55,
                'GradientBoosting': 0.45
            }
    
    predictions = {}
    for name, model in models.items():
        predictions[name] = model.predict(X_test)
    
    # Weighted ensemble
    ensemble_pred = np.zeros(len(X_test))
    total_weight = 0
    for name, pred in predictions.items():
        if name in weights:
            ensemble_pred += predictions[name] * weights[name]
            total_weight += weights[name]
        else:
            # If model not in weights dict, use equal weight
            remaining_weight = 1.0 - total_weight
            ensemble_pred += predictions[name] * (remaining_weight / (len(models) - len(weights)))
    
    # Calculate confidence based on prediction agreement
    pred_matrix = np.array(list(predictions.values()))
    std_dev = np.std(pred_matrix, axis=0)
    avg_std = np.mean(std_dev)
    
    # Normalize confidence to 0-1 (lower std = higher confidence)
    max_expected_std = np.mean(np.abs(ensemble_pred)) * 0.08  # 8% of mean as max expected std
    confidence = np.clip(1 - (avg_std / max_expected_std), 0, 1)
    
    # Boost confidence if all models agree on direction
    if len(predictions) >= 2:
        pred_signs = np.array([np.sign(p - X_test[:, 0]) for p in predictions.values()])
        agreement = np.mean(np.abs(np.mean(pred_signs, axis=0)))
        confidence = confidence * 0.7 + agreement * 0.3  # Blend agreement into confidence
    
    return ensemble_pred, predictions, confidence


def generate_investment_analysis(stock_ticker, forecast_days=30):
    """
    Generate comprehensive investment analysis with advanced ML ensemble prediction and scoring.
    Uses multiple models (AutoReg, RandomForest, GradientBoosting) for robust predictions.
    
    Returns:
        dict: Complete analysis including predictions, scores, and recommendations
    """
    try:
        # Fetch historical data with volume
        stock_data = fetch_stock_history(stock_ticker, period="2y")
        
        # Engineer advanced features
        stock_data_enhanced = engineer_features(stock_data)
        
        # Prepare close prices for AutoReg (time series)
        close_prices = stock_data_enhanced['Close'].asfreq('D', method='ffill')
        
        # Ensure enough data
        if len(close_prices) < 250:
            raise ValueError("Not enough historical data available for this stock to generate predictions.")
        
        # ========== PART 1: AutoReg Model (Time Series) ==========
        train_size = int(0.85 * len(close_prices))
        train_data_ar = close_prices.iloc[:train_size]
        test_data_ar = close_prices.iloc[train_size:]
        
        # Fit AutoReg model
        ar_model = AutoReg(train_data_ar, lags=min(60, len(train_data_ar) - 1)).fit()
        
        # Predict on test data
        predictions_ar = ar_model.predict(start=test_data_ar.index[0], end=test_data_ar.index[-1], dynamic=False)
        
        # Predict future values
        forecast_index = pd.date_range(start=test_data_ar.index[-1] + pd.Timedelta(days=1), 
                                       periods=forecast_days, freq='D')
        forecast_ar = ar_model.predict(start=len(close_prices), end=len(close_prices) + forecast_days - 1)
        forecast_ar = pd.Series(forecast_ar, index=forecast_index)
        
        # ========== PART 2: ML Ensemble Models (Feature-based) ==========
        try:
            X, y, feature_names, close_vals = prepare_ml_features(stock_data_enhanced, lookback=60)
            
            # Train-test split (time series aware)
            train_size_ml = int(0.85 * len(X))
            X_train, X_test = X[:train_size_ml], X[train_size_ml:]
            y_train, y_test = y[:train_size_ml], y[train_size_ml:]
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train ensemble models
            ensemble_models = train_ensemble_models(X_train_scaled, y_train)
            
            # Make predictions
            ensemble_pred, individual_preds, model_confidence = ensemble_predict(ensemble_models, X_test_scaled)
            
            # For next-day prediction, use the last data point
            last_features = X[-1:].reshape(1, -1)
            last_features_scaled = scaler.transform(last_features)
            next_day_pred_ml, individual_preds, conf = ensemble_predict(ensemble_models, last_features_scaled)
            predicted_price_ml = next_day_pred_ml[0]
            
            # Calculate model accuracy metrics for all available models
            mae_rf = mean_absolute_error(y_test, individual_preds['RandomForest'])
            mae_gb = mean_absolute_error(y_test, individual_preds['GradientBoosting'])
            mae_xgb = mean_absolute_error(y_test, individual_preds['XGBoost']) if 'XGBoost' in individual_preds else 0
            r2_rf = r2_score(y_test, individual_preds['RandomForest'])
            r2_gb = r2_score(y_test, individual_preds['GradientBoosting'])
            r2_xgb = r2_score(y_test, individual_preds['XGBoost']) if 'XGBoost' in individual_preds else 0
            
            ml_success = True
            
        except Exception as e:
            # Fallback to AutoReg if ML fails
            print(f"ML ensemble fallback: {e}")
            predicted_price_ml = forecast_ar.iloc[0]
            model_confidence = 0.5
            mae_rf = mae_gb = mae_xgb = 0
            r2_rf = r2_gb = r2_xgb = 0
            ml_success = False
        
        # ========== PART 3: Combine Predictions ==========
        current_price = close_prices.iloc[-1]
        
        # Weight predictions: 70% ML ensemble (improved!), 30% AutoReg (if ML successful)
        # Increased ML weight due to enhanced models and XGBoost addition
        if ml_success:
            predicted_price = 0.70 * predicted_price_ml + 0.30 * forecast_ar.iloc[0]
            final_confidence = model_confidence
        else:
            predicted_price = forecast_ar.iloc[0]
            final_confidence = 0.5
        
        predicted_return = ((predicted_price - current_price) / current_price) * 100
        
        # ========== PART 4: Get Latest Indicators ==========
        latest_data = stock_data_enhanced.iloc[-1]
        
        # Calculate investment score with advanced indicators
        score, breakdown = calculate_investment_score(
            predicted_return=predicted_return,
            current_price=current_price,
            ma_5=latest_data['MA_5'],
            ma_10=latest_data['MA_10'],
            ma_20=latest_data['MA_20'],
            volatility=latest_data['Volatility_10'],
            volume_ratio=latest_data['Volume_Ratio'],
            rsi=latest_data['RSI_14'] if 'RSI_14' in latest_data else None,
            macd_diff=latest_data['MACD_Diff'] if 'MACD_Diff' in latest_data else None,
            bb_position=latest_data['BB_Position'] if 'BB_Position' in latest_data else None,
            ma_50=latest_data['MA_50'] if 'MA_50' in latest_data else None,
            ma_200=latest_data['MA_200'] if 'MA_200' in latest_data else None,
            model_confidence=final_confidence
        )
        
        # Get recommendation (pass predicted return for lenient logic)
        decision, recommendation, color = get_investment_recommendation(score, predicted_return)
        
        # ========== PART 5: Detect Peak and When to Sell ==========
        sell_signal = None
        sell_reason = None
        peak_detected = False
        
        # Analyze the forecast for peak detection
        if len(forecast_ar) > 1:
            forecast_values = forecast_ar.values
            # Find if there's a peak (price goes up then down)
            for i in range(1, len(forecast_values) - 1):
                if forecast_values[i] > forecast_values[i-1] and forecast_values[i] > forecast_values[i+1]:
                    peak_detected = True
                    days_to_peak = i + 1
                    peak_price = forecast_values[i]
                    peak_return = ((peak_price - current_price) / current_price) * 100
                    
                    sell_signal = {
                        'days_to_peak': days_to_peak,
                        'peak_price': peak_price,
                        'peak_return': peak_return,
                        'sell_date': forecast_ar.index[i]
                    }
                    
                    if peak_return > 2:
                        sell_reason = f"📊 Peak expected in {days_to_peak} day(s) at ${peak_price:.2f} (+{peak_return:.1f}%)"
                    else:
                        sell_reason = f"⚠️ Small peak in {days_to_peak} day(s), consider holding longer"
                    break
        
        # Check for downtrend signals
        if not peak_detected:
            # Check if RSI is overbought
            if 'RSI_14' in latest_data and latest_data['RSI_14'] > 70:
                sell_signal = {
                    'type': 'overbought',
                    'rsi': latest_data['RSI_14']
                }
                sell_reason = f"⚠️ RSI Overbought ({latest_data['RSI_14']:.1f}) - consider taking profits soon"
            
            # Check if near upper Bollinger Band
            elif 'BB_Position' in latest_data and latest_data['BB_Position'] > 0.85:
                sell_signal = {
                    'type': 'bb_upper',
                    'bb_position': latest_data['BB_Position']
                }
                sell_reason = "⚠️ Near upper Bollinger Band - may pullback"
            
            # Check if Death Cross forming
            elif latest_data.get('MA_50', 0) < latest_data.get('MA_200', 0):
                sell_signal = {
                    'type': 'death_cross'
                }
                sell_reason = "⚠️ Death Cross (MA50 < MA200) - bearish signal"
        
        # ========== PART 6: Generate Detailed Reasons ==========
        reasons = []
        
        # Prediction-based reasons
        if predicted_return > 1.5:
            reasons.append(f"📈 Strong predicted return (+{predicted_return:.2f}%)")
        elif predicted_return > 0:
            reasons.append(f"📊 Positive predicted return (+{predicted_return:.2f}%)")
        elif predicted_return < -1.0:
            reasons.append(f"📉 Negative predicted return ({predicted_return:.2f}%)")
        
        # Trend-based reasons
        if latest_data['Price_Above_MA20'] and latest_data['Price_Above_MA50']:
            reasons.append("🔼 Strong upward trend (above key MAs)")
        elif latest_data['MA_50_200_Cross'] == 1:
            reasons.append("⭐ Golden Cross detected (MA50 > MA200)")
        
        # RSI-based reasons
        if 'RSI_14' in latest_data:
            rsi_val = latest_data['RSI_14']
            if rsi_val < 30:
                reasons.append(f"💎 RSI Oversold ({rsi_val:.1f}) - potential bounce")
            elif rsi_val > 70:
                reasons.append(f"⚠️ RSI Overbought ({rsi_val:.1f}) - caution")
            elif 40 <= rsi_val <= 60:
                reasons.append(f"✅ RSI Neutral ({rsi_val:.1f}) - healthy")
        
        # MACD-based reasons
        if 'MACD_Diff' in latest_data and latest_data['MACD_Diff'] > 0:
            reasons.append("⚡ MACD bullish momentum")
        
        # Volatility-based reasons
        if latest_data['Volatility_10'] < 1.5:
            reasons.append(f"🛡️ Low volatility ({latest_data['Volatility_10']:.2f}%) - stable")
        elif latest_data['Volatility_10'] > 4.0:
            reasons.append(f"⚠️ High volatility ({latest_data['Volatility_10']:.2f}%) - risky")
        
        # Volume-based reasons
        if latest_data['Volume_Ratio'] > 1.5:
            reasons.append(f"📊 Strong volume ({latest_data['Volume_Ratio']:.2f}x avg)")
        elif latest_data['Volume_Ratio'] < 0.7:
            reasons.append(f"⚠️ Low volume ({latest_data['Volume_Ratio']:.2f}x avg)")
        
        # Bollinger Bands
        if 'BB_Position' in latest_data:
            bb_pos = latest_data['BB_Position']
            if bb_pos < 0.2:
                reasons.append("📍 Near lower Bollinger Band - oversold")
            elif bb_pos > 0.8:
                reasons.append("📍 Near upper Bollinger Band - overbought")
        
        # Model confidence
        if ml_success and final_confidence > 0.7:
            reasons.append(f"🎯 High model confidence ({final_confidence*100:.0f}%)")
        elif ml_success and final_confidence < 0.4:
            reasons.append(f"⚠️ Low model confidence ({final_confidence*100:.0f}%)")
        
        if not reasons:
            reasons.append("⚠️ Mixed signals - proceed with caution")
        
        # ========== PART 6: Calculate Exit Timing ==========
        exit_timing = calculate_exit_timing(
            forecast=forecast_ar,
            current_price=current_price,
            indicators=latest_data
        )
        
        # ========== PART 7: Compile Analysis ==========
        analysis = {
            'train_data': train_data_ar,
            'test_data': test_data_ar,
            'predictions': predictions_ar,
            'forecast': forecast_ar,
            'current_price': current_price,
            'predicted_price': predicted_price,
            'predicted_return': predicted_return,
            'investment_score': score,
            'score_breakdown': breakdown,
            'decision': decision,
            'recommendation': recommendation,
            'color': color,
            'reasons': reasons,
            'model_confidence': final_confidence,
            'ml_success': ml_success,
            'exit_signal': exit_timing['signal'],
            'exit_date': exit_timing['date'],
            'exit_reason': exit_timing['reason'],
            'exit_confidence': exit_timing['confidence'],
            'latest_indicators': {
                'MA_5': latest_data['MA_5'],
                'MA_10': latest_data['MA_10'],
                'MA_20': latest_data['MA_20'],
                'MA_50': latest_data['MA_50'] if 'MA_50' in latest_data else None,
                'MA_200': latest_data['MA_200'] if 'MA_200' in latest_data else None,
                'RSI_14': latest_data['RSI_14'] if 'RSI_14' in latest_data else None,
                'MACD_Diff': latest_data['MACD_Diff'] if 'MACD_Diff' in latest_data else None,
                'Volatility': latest_data['Volatility_10'],
                'Volume_Ratio': latest_data['Volume_Ratio'],
                'BB_Position': latest_data['BB_Position'] if 'BB_Position' in latest_data else None
            }
        }
        
        # Add model metrics if ML was successful
        if ml_success:
            analysis['model_metrics'] = {
                'RandomForest_MAE': round(mae_rf, 2),
                'GradientBoosting_MAE': round(mae_gb, 2),
                'XGBoost_MAE': round(mae_xgb, 2),
                'RandomForest_R2': round(r2_rf, 3),
                'GradientBoosting_R2': round(r2_gb, 3),
                'XGBoost_R2': round(r2_xgb, 3)
            }
        
        return analysis
        
    except ValueError as ve:
        raise ValueError(ve)
    except Exception as e:
        raise Exception(f"Error generating investment analysis: {e}")


def generate_stock_prediction(stock_ticker, forecast_days=30):
    """
    Generate stock price predictions using AutoReg model (legacy function for compatibility).
    Args:
        stock_ticker (str): The stock ticker symbol.
        forecast_days (int): The number of days to forecast.
    Returns:
        tuple: Training data, test data, predictions, and forecast values.
    """
    try:
        # Fetch the last 2 years of historical stock data
        stock_data = fetch_stock_history(stock_ticker, period="2y")

        # Prepare the close prices data
        close_prices = stock_data['Close'].asfreq('D', method='ffill')

        # Ensure there's enough data for the model
        if len(close_prices) < 250:  # Minimum data required for lags
            raise ValueError("Not enough historical data available for this stock to generate predictions.")

        # Split the data into train and test sets
        train_data = close_prices.iloc[:int(0.9 * len(close_prices))]
        test_data = close_prices.iloc[int(0.9 * len(close_prices)):]

        # Fit the AutoReg model
        model = AutoReg(train_data, lags=min(250, len(train_data) - 1)).fit()

        # Predict on the test data
        predictions = model.predict(start=test_data.index[0], end=test_data.index[-1], dynamic=True)

        # Predict future values
        forecast_index = pd.date_range(start=test_data.index[-1] + pd.Timedelta(days=1), periods=forecast_days, freq='D')
        forecast = model.predict(start=len(close_prices), end=len(close_prices) + forecast_days - 1)
        forecast = pd.Series(forecast, index=forecast_index)

        return train_data, test_data, predictions, forecast

    except ValueError as ve:
        raise ValueError(ve)  # Raise user-friendly warnings
    except Exception as e:
        raise Exception(f"Error generating prediction: {e}")


def get_smart_investment_recommendation(top_stocks=None, progress_callback=None):
    """
    Analyze multiple top stocks and recommend the best investment opportunity.
    
    Args:
        top_stocks (list): List of stock tickers to analyze. If None, uses default top stocks.
        progress_callback (function): Optional callback to report progress
    
    Returns:
        dict: {
            'recommended_stock': str (ticker),
            'company_name': str,
            'score': float,
            'confidence': float,
            'predicted_return': float,
            'recommendation': str,
            'reasons': list,
            'all_analyses': list (all stock results sorted by score)
        }
    """
    if top_stocks is None:
        # Default to analyzing top 10 popular stocks
        top_stocks = [
            'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 
            'META', 'TSLA', 'JPM', 'V', 'JNJ'
        ]
    
    all_results = []
    
    for i, ticker in enumerate(top_stocks):
        try:
            if progress_callback:
                progress_callback(i + 1, len(top_stocks), ticker)
            
            # Analyze the stock
            analysis = generate_investment_analysis(ticker, forecast_days=5)
            
            # Extract key metrics
            result = {
                'ticker': ticker,
                'score': analysis['investment_score'],
                'confidence': analysis.get('model_confidence', 0.5),
                'predicted_return': analysis['predicted_return'],
                'recommendation': analysis['recommendation'],
                'decision': analysis['decision'],
                'color': analysis['color'],
                'reasons': analysis['reasons'][:3],  # Top 3 reasons
                'current_price': analysis['current_price'],
                'predicted_price': analysis['predicted_price']
            }
            
            all_results.append(result)
            
        except Exception as e:
            # Skip stocks that fail to analyze
            print(f"Skipping {ticker}: {str(e)}")
            continue
    
    # Sort by score (descending) and confidence
    all_results.sort(key=lambda x: (x['score'], x['confidence']), reverse=True)
    
    if not all_results:
        return None
    
    # Get the best stock
    best_stock = all_results[0]
    
    # Get company name
    try:
        sp_tickers = fetch_sp_tickers()
        company_name = sp_tickers.get(best_stock['ticker'], best_stock['ticker'])
    except:
        company_name = best_stock['ticker']
    
    return {
        'recommended_stock': best_stock['ticker'],
        'company_name': company_name,
        'score': best_stock['score'],
        'confidence': best_stock['confidence'],
        'predicted_return': best_stock['predicted_return'],
        'recommendation': best_stock['recommendation'],
        'decision': best_stock['decision'],
        'color': best_stock['color'],
        'reasons': best_stock['reasons'],
        'current_price': best_stock['current_price'],
        'predicted_price': best_stock['predicted_price'],
        'all_analyses': all_results  # Include all for comparison
    }
