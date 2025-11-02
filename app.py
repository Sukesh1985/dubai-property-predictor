import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config MUST be first
st.set_page_config(
    page_title="Dubai Property Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode with toggle
def local_css():
    dark_mode = st.session_state.get('dark_mode', False)
    
    if dark_mode:
        # Dark theme colors
        bg_color = "#0e1117"
        secondary_bg = "#262730"
        text_color = "#fafafa"
        border_color = "#444"
    else:
        # Light theme colors
        bg_color = "#ffffff"
        secondary_bg = "#f0f2f6"
        text_color = "#262730"
        border_color = "#ddd"
    
    st.markdown(f"""
        <style>
        /* Main app styling */
        .stApp {{
            background-color: {bg_color};
        }}
        
        /* Metric cards */
        [data-testid="stMetricValue"] {{
            color: {text_color};
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
        }}
        
        /* Text */
        p, div, span, label {{
            color: {text_color};
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {secondary_bg};
        }}
        
        /* Input fields */
        .stTextInput input, .stNumberInput input, .stSelectbox select {{
            background-color: {secondary_bg} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
        }}
        
        /* Buttons */
        .stButton button {{
            background-color: #1f4788 !important;
            color: white !important;
            border: none !important;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            font-weight: 600;
        }}
        
        .stButton button:hover {{
            background-color: #2c5aa0 !important;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        /* Cards */
        .prediction-card {{
            background: linear-gradient(135deg, #1f4788 0%, #2c5aa0 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin: 2rem 0;
        }}
        
        /* Info boxes */
        .info-box {{
            background-color: {secondary_bg};
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #1f4788;
            margin: 1rem 0;
        }}
        
        /* Dark mode toggle */
        .dark-mode-toggle {{
            position: fixed;
            top: 70px;
            right: 20px;
            z-index: 999;
            background-color: {secondary_bg};
            padding: 10px;
            border-radius: 50%;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            cursor: pointer;
        }}
        </style>
    """, unsafe_allow_html=True)

# Initialize session state for dark mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode

# Apply CSS
local_css()

# Load model and data
@st.cache_resource
def load_model():
    try:
        with open('dubai_property_model.pkl', 'rb') as file:
            return pickle.load(file)
    except:
        st.error("Model file not found. Please ensure 'dubai_property_model.pkl' is in the app directory.")
        return None

@st.cache_data
def load_data():
    try:
        return pd.read_csv('dubai_properties_final.csv')
    except:
        st.error("Data file not found. Please ensure 'dubai_properties_final.csv' is in the app directory.")
        return None

model = load_model()
df = load_data()

# Sidebar with dark mode toggle
with st.sidebar:
    # Dark mode toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### ⚙️ Settings")
    with col2:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 🧭 Navigation")
    page = st.radio("", 
                    ["🏠 Home", "🔮 Price Predictor", "📊 Market Insights", "💰 Investment Calculator"],
                    label_visibility="collapsed")

# Main content based on selected page
if page == "🏠 Home":
    st.markdown("""
        <div style='text-align: center;'>
            <h1>🏠 Dubai Real Estate Price Predictor</h1>
            <p style='font-size: 1.2em; opacity: 0.8;'>
                AI-Powered Property Valuation & Market Analysis
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats
    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Properties", f"{len(df):,}")
        with col2:
            st.metric("Average Price", f"AED {df['price'].mean():,.0f}")
        with col3:
            st.metric("Locations", df['location'].nunique())
        with col4:
            st.metric("Property Types", df['property_type'].nunique())
    
    st.markdown("---")
    
    # Features
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class='info-box'>
                <h3>🔮 Price Prediction</h3>
                <p>Get instant property valuations using advanced ML algorithms</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='info-box'>
                <h3>📊 Market Insights</h3>
                <p>Explore trends, comparisons, and market analysis</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='info-box'>
                <h3>💰 ROI Calculator</h3>
                <p>Calculate investment returns and rental yields</p>
            </div>
        """, unsafe_allow_html=True)

elif page == "🔮 Price Predictor":
    st.title("🔮 Property Price Predictor")
    
    if model is None or df is None:
        st.error("Required files not loaded. Cannot make predictions.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.selectbox("📍 Location", sorted(df['location'].unique()))
            property_type = st.selectbox("🏢 Property Type", sorted(df['property_type'].unique()))
            size_sqft = st.number_input("📏 Size (sq.ft)", min_value=100, max_value=20000, value=1000, step=100)
        
        with col2:
            bedrooms = st.number_input("🛏️ Bedrooms", min_value=0, max_value=10, value=2)
            bathrooms = st.number_input("🚿 Bathrooms", min_value=1, max_value=10, value=2)
            quality = st.selectbox("⭐ Quality", ['Standard', 'Premium', 'Luxury'])
        
        if st.button("🔮 Predict Price", use_container_width=True):
            # Prepare features
            features = pd.DataFrame({
                'location': [location],
                'property_type': [property_type],
                'size_sqft': [size_sqft],
                'bedrooms': [bedrooms],
                'bathrooms': [bathrooms],
                'quality': [quality]
            })
            
            # Make prediction
            predicted_price = model.predict(features)[0]
            
            # Display result
            st.markdown(f"""
                <div class='prediction-card'>
                    <h2>Predicted Property Price</h2>
                    <h1 style='font-size: 3em; margin: 1rem 0;'>
                        AED {predicted_price:,.0f}
                    </h1>
                    <p style='font-size: 1.2em; opacity: 0.9;'>
                        Price per sq.ft: AED {predicted_price/size_sqft:,.0f}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Additional insights
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Lower Estimate (-10%)", f"AED {predicted_price * 0.9:,.0f}")
            with col2:
                st.metric("Predicted Price", f"AED {predicted_price:,.0f}")
            with col3:
                st.metric("Upper Estimate (+10%)", f"AED {predicted_price * 1.1:,.0f}")

elif page == "📊 Market Insights":
    st.title("📊 Market Insights")
    
    if df is not None:
        tab1, tab2, tab3 = st.tabs(["📈 Price Trends", "📍 Location Analysis", "🏢 Property Types"])
        
        with tab1:
            # Average price by location
            avg_prices = df.groupby('location')['price'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(x=avg_prices.index, y=avg_prices.values,
                        labels={'x': 'Location', 'y': 'Average Price (AED)'},
                        title='Top 10 Locations by Average Price')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Property distribution by location
            location_counts = df['location'].value_counts().head(10)
            fig = px.pie(values=location_counts.values, names=location_counts.index,
                        title='Property Distribution - Top 10 Locations')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Price by property type
            type_prices = df.groupby('property_type')['price'].mean().sort_values(ascending=False)
            fig = px.bar(x=type_prices.index, y=type_prices.values,
                        labels={'x': 'Property Type', 'y': 'Average Price (AED)'},
                        title='Average Price by Property Type')
            st.plotly_chart(fig, use_container_width=True)

elif page == "💰 Investment Calculator":
    st.title("💰 Investment Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        purchase_price = st.number_input("💵 Purchase Price (AED)", 
                                        min_value=100000, max_value=50000000, 
                                        value=1000000, step=50000)
        
        annual_rent = st.number_input("🏠 Expected Annual Rent (AED)", 
                                     min_value=10000, max_value=5000000, 
                                     value=80000, step=10000)
        
        down_payment_pct = st.slider("💰 Down Payment %", 0, 100, 25)
    
    with col2:
        loan_interest = st.slider("📊 Loan Interest Rate %", 0.0, 10.0, 4.5, 0.1)
        loan_years = st.slider("📅 Loan Period (years)", 1, 30, 20)
        appreciation = st.slider("📈 Annual Appreciation %", 0.0, 15.0, 5.0, 0.5)
    
    if st.button("💡 Calculate Returns", use_container_width=True):
        # Calculations
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        
        monthly_rate = (loan_interest / 100) / 12
        num_payments = loan_years * 12
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                         ((1 + monthly_rate)**num_payments - 1) if monthly_rate > 0 else loan_amount / num_payments
        
        annual_mortgage = monthly_payment * 12
        rental_yield = (annual_rent / purchase_price) * 100
        net_rental_income = annual_rent - annual_mortgage
        roi = (net_rental_income / down_payment) * 100
        
        future_value = purchase_price * (1 + appreciation/100)**5
        capital_gain = future_value - purchase_price
        
        # Display results
        st.markdown("### 📊 Investment Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Rental Yield", f"{rental_yield:.2f}%")
        with col2:
            st.metric("ROI", f"{roi:.2f}%")
        with col3:
            st.metric("Monthly Payment", f"AED {monthly_payment:,.0f}")
        with col4:
            st.metric("Net Annual Income", f"AED {net_rental_income:,.0f}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class='info-box'>
                    <h3>💰 Initial Investment</h3>
                    <p style='font-size: 1.5em;'><strong>AED {down_payment:,.0f}</strong></p>
                    <p>Down Payment ({down_payment_pct}%)</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='info-box'>
                    <h3>📈 5-Year Projection</h3>
                    <p style='font-size: 1.5em;'><strong>AED {capital_gain:,.0f}</strong></p>
                    <p>Capital Appreciation ({appreciation}% annual)</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; opacity: 0.7;'>
        <p>Built by Sukesh Singla | HR Analytics Specialist</p>
        <p>🌐 <a href='https://sukesh1985.github.io' target='_blank'>Portfolio</a> | 
           💼 <a href='https://linkedin.com/in/sukesh-singla-667701a5' target='_blank'>LinkedIn</a> | 
           📧 ssingla25@gmail.com</p>
    </div>
""", unsafe_allow_html=True)
