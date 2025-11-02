import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Dubai Property Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize dark mode in session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# CSS for BOTH themes with proper toggle
def apply_theme():
    if st.session_state.dark_mode:
        # DARK THEME
        st.markdown("""
            <style>
            /* Dark Theme */
            .stApp {
                background-color: #0e1117 !important;
            }
            .stApp > header {
                background-color: #0e1117 !important;
            }
            [data-testid="stSidebar"] {
                background-color: #262730 !important;
            }
            [data-testid="stSidebar"] > div:first-child {
                background-color: #262730 !important;
            }
            p, h1, h2, h3, h4, h5, h6, span, div, label {
                color: #fafafa !important;
            }
            [data-testid="stMetricValue"] {
                color: #fafafa !important;
            }
            [data-testid="stMetricLabel"] {
                color: #fafafa !important;
            }
            .stMarkdown {
                color: #fafafa !important;
            }
            input, select, textarea {
                background-color: #262730 !important;
                color: #fafafa !important;
                border: 1px solid #444 !important;
            }
            [data-baseweb="select"] {
                background-color: #262730 !important;
            }
            [data-baseweb="base-input"] {
                background-color: #262730 !important;
            }
            .stButton button {
                background-color: #1f4788 !important;
                color: white !important;
                border: none !important;
            }
            .stButton button:hover {
                background-color: #2c5aa0 !important;
            }
            /* Plotly dark theme */
            .js-plotly-plot {
                background-color: #0e1117 !important;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        # LIGHT THEME
        st.markdown("""
            <style>
            /* Light Theme */
            .stApp {
                background-color: #ffffff !important;
            }
            .stApp > header {
                background-color: #ffffff !important;
            }
            [data-testid="stSidebar"] {
                background-color: #f0f2f6 !important;
            }
            [data-testid="stSidebar"] > div:first-child {
                background-color: #f0f2f6 !important;
            }
            p, h1, h2, h3, h4, h5, h6, span, div, label {
                color: #262730 !important;
            }
            [data-testid="stMetricValue"] {
                color: #262730 !important;
            }
            [data-testid="stMetricLabel"] {
                color: #262730 !important;
            }
            .stMarkdown {
                color: #262730 !important;
            }
            input, select, textarea {
                background-color: #ffffff !important;
                color: #262730 !important;
                border: 1px solid #ddd !important;
            }
            [data-baseweb="select"] {
                background-color: #ffffff !important;
            }
            [data-baseweb="base-input"] {
                background-color: #ffffff !important;
            }
            .stButton button {
                background-color: #1f4788 !important;
                color: white !important;
                border: none !important;
            }
            .stButton button:hover {
                background-color: #2c5aa0 !important;
            }
            </style>
        """, unsafe_allow_html=True)

# Apply current theme
apply_theme()

# Common CSS for both themes
st.markdown("""
    <style>
    .prediction-card {
        background: linear-gradient(135deg, #1f4788 0%, #2c5aa0 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 2rem 0;
    }
    .prediction-card h1, .prediction-card h2, .prediction-card p {
        color: white !important;
    }
    .stButton button {
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# Load model and data
@st.cache_resource
def load_model():
    try:
        with open('dubai_property_model.pkl', 'rb') as file:
            return pickle.load(file)
    except:
        return None

@st.cache_data
def load_data():
    try:
        return pd.read_csv('dubai_properties_final.csv')
    except:
        return None

model = load_model()
df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Dark mode toggle button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Theme")
    with col2:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "Select a page",
        ["🏠 Home", "🔮 Price Predictor", "📊 Market Insights", "💰 Investment Calculator"],
        label_visibility="collapsed"
    )

# MAIN CONTENT
if page == "🏠 Home":
    st.title("🏠 Dubai Real Estate Price Predictor")
    st.markdown("### AI-Powered Property Valuation & Market Analysis")
    
    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Properties", f"{len(df):,}")
        with col2:
            st.metric("Avg Price", f"AED {df['price'].mean():,.0f}")
        with col3:
            st.metric("Locations", df['location'].nunique())
        with col4:
            st.metric("Property Types", df['property_type'].nunique())
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🔮 Price Prediction")
        st.write("Get instant property valuations using ML")
    with col2:
        st.markdown("#### 📊 Market Insights")
        st.write("Explore trends and analysis")
    with col3:
        st.markdown("#### 💰 ROI Calculator")
        st.write("Calculate investment returns")

elif page == "🔮 Price Predictor":
    st.title("🔮 Property Price Predictor")
    
    if model is None or df is None:
        st.error("Model or data not loaded")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.selectbox("📍 Location", sorted(df['location'].unique()))
            property_type = st.selectbox("🏢 Property Type", sorted(df['property_type'].unique()))
            size_sqft = st.number_input("📏 Size (sq.ft)", 100, 20000, 1000, 100)
        
        with col2:
            bedrooms = st.number_input("🛏️ Bedrooms", 0, 10, 2)
            bathrooms = st.number_input("🚿 Bathrooms", 1, 10, 2)
            quality = st.selectbox("⭐ Quality", ['Standard', 'Premium', 'Luxury'])
        
        if st.button("🔮 Predict Price", use_container_width=True):
            features = pd.DataFrame({
                'location': [location],
                'property_type': [property_type],
                'size_sqft': [size_sqft],
                'bedrooms': [bedrooms],
                'bathrooms': [bathrooms],
                'quality': [quality]
            })
            
            predicted_price = model.predict(features)[0]
            
            st.markdown(f"""
                <div class='prediction-card'>
                    <h2>Predicted Property Price</h2>
                    <h1 style='font-size: 3em; margin: 1rem 0;'>
                        AED {predicted_price:,.0f}
                    </h1>
                    <p style='font-size: 1.2em;'>
                        Price per sq.ft: AED {predicted_price/size_sqft:,.0f}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Lower (-10%)", f"AED {predicted_price * 0.9:,.0f}")
            with col2:
                st.metric("Predicted", f"AED {predicted_price:,.0f}")
            with col3:
                st.metric("Upper (+10%)", f"AED {predicted_price * 1.1:,.0f}")

elif page == "📊 Market Insights":
    st.title("📊 Market Insights")
    
    if df is not None:
        tab1, tab2, tab3 = st.tabs(["📈 Price Trends", "📍 Locations", "🏢 Types"])
        
        with tab1:
            avg_prices = df.groupby('location')['price'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(x=avg_prices.index, y=avg_prices.values,
                        labels={'x': 'Location', 'y': 'Avg Price (AED)'},
                        title='Top 10 Locations by Average Price',
                        template='plotly_dark' if st.session_state.dark_mode else 'plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            location_counts = df['location'].value_counts().head(10)
            fig = px.pie(values=location_counts.values, names=location_counts.index,
                        title='Top 10 Locations by Property Count',
                        template='plotly_dark' if st.session_state.dark_mode else 'plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            type_prices = df.groupby('property_type')['price'].mean().sort_values(ascending=False)
            fig = px.bar(x=type_prices.index, y=type_prices.values,
                        labels={'x': 'Property Type', 'y': 'Avg Price (AED)'},
                        title='Average Price by Property Type',
                        template='plotly_dark' if st.session_state.dark_mode else 'plotly_white')
            st.plotly_chart(fig, use_container_width=True)

elif page == "💰 Investment Calculator":
    st.title("💰 Investment Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        purchase_price = st.number_input("💵 Purchase Price (AED)", 100000, 50000000, 1000000, 50000)
        annual_rent = st.number_input("🏠 Annual Rent (AED)", 10000, 5000000, 80000, 10000)
        down_payment_pct = st.slider("💰 Down Payment %", 0, 100, 25)
    
    with col2:
        loan_interest = st.slider("📊 Interest Rate %", 0.0, 10.0, 4.5, 0.1)
        loan_years = st.slider("📅 Loan Period (years)", 1, 30, 20)
        appreciation = st.slider("📈 Annual Appreciation %", 0.0, 15.0, 5.0, 0.5)
    
    if st.button("💡 Calculate Returns", use_container_width=True):
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        
        monthly_rate = (loan_interest / 100) / 12
        num_payments = loan_years * 12
        
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        else:
            monthly_payment = loan_amount / num_payments
        
        annual_mortgage = monthly_payment * 12
        rental_yield = (annual_rent / purchase_price) * 100
        net_rental_income = annual_rent - annual_mortgage
        roi = (net_rental_income / down_payment) * 100 if down_payment > 0 else 0
        
        future_value = purchase_price * (1 + appreciation/100)**5
        capital_gain = future_value - purchase_price
        
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
                #### 💰 Initial Investment
                **AED {down_payment:,.0f}**  
                Down Payment ({down_payment_pct}%)
            """)
        
        with col2:
            st.markdown(f"""
                #### 📈 5-Year Projection
                **AED {capital_gain:,.0f}**  
                Capital Appreciation ({appreciation}% annual)
            """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; opacity: 0.7;'>
        <p>Built by Sukesh Singla | HR Analytics Specialist</p>
        <p>🌐 <a href='https://sukesh1985.github.io'>Portfolio</a> | 
           💼 <a href='https://linkedin.com/in/sukesh-singla-667701a5'>LinkedIn</a> | 
           📧 ssingla25@gmail.com</p>
    </div>
""", unsafe_allow_html=True)
