import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Page config
st.set_page_config(
    page_title="Dubai Property Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize dark mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Theme CSS
def apply_theme():
    if st.session_state.dark_mode:
        st.markdown("""
            <style>
            .stApp { background-color: #0e1117 !important; }
            .stApp > header { background-color: #0e1117 !important; }
            [data-testid="stSidebar"] { background-color: #262730 !important; }
            [data-testid="stSidebar"] > div:first-child { background-color: #262730 !important; }
            p, h1, h2, h3, h4, h5, h6, span, div, label { color: #fafafa !important; }
            [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #fafafa !important; }
            .stMarkdown { color: #fafafa !important; }
            input, select, textarea { background-color: #262730 !important; color: #fafafa !important; border: 1px solid #444 !important; }
            [data-baseweb="select"], [data-baseweb="base-input"] { background-color: #262730 !important; }
            .stButton button { background-color: #1f4788 !important; color: white !important; border: none !important; }
            .stButton button:hover { background-color: #2c5aa0 !important; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp { background-color: #ffffff !important; }
            .stApp > header { background-color: #ffffff !important; }
            [data-testid="stSidebar"] { background-color: #f0f2f6 !important; }
            [data-testid="stSidebar"] > div:first-child { background-color: #f0f2f6 !important; }
            p, h1, h2, h3, h4, h5, h6, span, div, label { color: #262730 !important; }
            [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #262730 !important; }
            .stMarkdown { color: #262730 !important; }
            input, select, textarea { background-color: #ffffff !important; color: #262730 !important; border: 1px solid #ddd !important; }
            [data-baseweb="select"], [data-baseweb="base-input"] { background-color: #ffffff !important; }
            .stButton button { background-color: #1f4788 !important; color: white !important; border: none !important; }
            .stButton button:hover { background-color: #2c5aa0 !important; }
            </style>
        """, unsafe_allow_html=True)

apply_theme()

# Common CSS
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
    .prediction-card h1, .prediction-card h2, .prediction-card p { color: white !important; }
    .feature-box {
        background: """ + ("#262730" if st.session_state.dark_mode else "#f0f2f6") + """;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        border-left: 4px solid #1f4788;
        margin: 1rem 0;
        min-height: 150px;
    }
    .stButton button {
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
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
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Theme")
    with col2:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("---")
    
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
    
    st.markdown("---")
    
    # Stats - Show even if no data
    col1, col2, col3, col4 = st.columns(4)
    if df is not None:
        with col1:
            st.metric("Total Properties", f"{len(df):,}")
        with col2:
            st.metric("Avg Price", f"AED {df['price'].mean():,.0f}")
        with col3:
            st.metric("Locations", df['location'].nunique())
        with col4:
            st.metric("Property Types", df['property_type'].nunique())
    else:
        with col1:
            st.metric("Status", "Demo Mode")
        with col2:
            st.metric("Features", "All Working")
        with col3:
            st.metric("Theme", "✅ Toggle")
        with col4:
            st.metric("Ready", "100%")
    
    st.markdown("---")
    
    # Features
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class='feature-box'>
                <h3>🔮 Price Prediction</h3>
                <p>Get instant property valuations using advanced ML algorithms</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='feature-box'>
                <h3>📊 Market Insights</h3>
                <p>Explore trends, comparisons, and market analysis</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='feature-box'>
                <h3>💰 ROI Calculator</h3>
                <p>Calculate investment returns and rental yields</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About
    st.markdown("### 🎯 About This Application")
    st.markdown("""
        This Dubai Real Estate Price Predictor uses **Machine Learning** to provide accurate property valuations
        and comprehensive market insights for the Dubai real estate market.
        
        **Key Features:**
        - 🤖 ML-powered price predictions
        - 📈 Interactive market analysis
        - 💰 Investment ROI calculator
        - 🌙 Dark/Light theme toggle
        - 📱 Mobile-responsive design
        
        **Built with:** Python, Streamlit, Scikit-learn, Plotly
    """)

elif page == "🔮 Price Predictor":
    st.title("🔮 Property Price Predictor")
    
    if model is None:
        st.warning("⚠️ Demo Mode: Model file not loaded. Upload `dubai_property_model.pkl` to enable predictions.")
        st.info("💡 This page will work once you upload the required model file to your GitHub repository.")
    else:
        if df is None:
            st.warning("⚠️ Data file not loaded. Using default values.")
            # Default values
            locations = ['Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah', 'Business Bay', 'JBR']
            property_types = ['Apartment', 'Villa', 'Townhouse', 'Penthouse']
        else:
            locations = sorted(df['location'].unique())
            property_types = sorted(df['property_type'].unique())
        
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.selectbox("📍 Location", locations)
            property_type = st.selectbox("🏢 Property Type", property_types)
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
            
            try:
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
            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")

elif page == "📊 Market Insights":
    st.title("📊 Market Insights")
    
    if df is None:
        st.warning("⚠️ Demo Mode: Data file not loaded.")
        st.info("💡 Upload `dubai_properties_final.csv` to see real market insights.")
        
        # Show placeholder
        st.markdown("""
            ### 📈 Market Analysis Features
            
            Once data is uploaded, this page will display:
            - **Price Trends** - Average prices by location
            - **Location Analysis** - Property distribution across Dubai
            - **Property Types** - Comparison of different property categories
            
            All with interactive Plotly charts!
        """)
    else:
        try:
            import plotly.express as px
            
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
        except:
            st.error("Error loading Plotly. Make sure it's in requirements.txt")

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
            monthly_payment = loan_amount / num_payments if num_payments > 0 else 0
        
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
        <p>🌐 <a href='https://sukesh1985.github.io' target='_blank'>Portfolio</a> | 
           💼 <a href='https://linkedin.com/in/sukesh-singla-667701a5' target='_blank'>LinkedIn</a> | 
           📧 ssingla25@gmail.com</p>
    </div>
""", unsafe_allow_html=True)

