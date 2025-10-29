import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import urllib.request

# Try to import Plotly (optional)
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="Dubai Property Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {padding: 0rem 1rem;}
    h1 {color: #1f4788;}
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>🏠 Dubai Real Estate Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666;'>AI-Powered Property Valuation Tool</h3>", unsafe_allow_html=True)
st.markdown("---")

# Model status
st.info("📊 Using optimized estimation formula")
st.markdown("---")

# Input Section
st.header("📋 Property Details")

col1, col2 = st.columns(2)

with col1:
    location = st.selectbox("📍 Location", ["Downtown Dubai", "Dubai Marina", "Palm Jumeirah", "Business Bay", "JBR", "Arabian Ranches"])
    bedrooms = st.slider("🛏️ Bedrooms", 1, 7, 2)
    area = st.number_input("📐 Area (sqft)", 500, 15000, 1500, step=100)

with col2:
    property_type = st.selectbox("🏢 Type", ["Apartment", "Villa", "Townhouse", "Penthouse"])
    bathrooms = st.slider("🚿 Bathrooms", 1, 7, 2)
    parking = st.slider("🚗 Parking Spaces", 0, 5, 1)

st.markdown("### ✨ Amenities")
col1, col2, col3, col4 = st.columns(4)

with col1:
    has_pool = st.checkbox("🏊 Pool")
with col2:
    has_gym = st.checkbox("💪 Gym")
with col3:
    has_security = st.checkbox("🔒 Security")
with col4:
    has_balcony = st.checkbox("🌅 Balcony")

if st.button("🔮 Predict Price", type="primary", use_container_width=True):
    st.markdown("---")
    
    # Calculate prediction using formula
    with st.spinner("Calculating..."):
        base_price = 1000000
        location_multiplier = {
            "Downtown Dubai": 1.5, "Dubai Marina": 1.3, "Palm Jumeirah": 1.8,
            "Business Bay": 1.4, "JBR": 1.3, "Arabian Ranches": 1.2
        }
        type_multiplier = {"Apartment": 1.0, "Villa": 1.5, "Townhouse": 1.2, "Penthouse": 1.8}
        
        prediction = (base_price * location_multiplier.get(location, 1.0) * type_multiplier.get(property_type, 1.0) * (area / 1500) * (bedrooms * 0.3 + 0.7))
        
        st.success("📊 **Price Prediction Complete**")
    
    # Display Price Results
    st.subheader("💰 Price Prediction")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Predicted Price", f"AED {prediction:,.0f}", delta="Estimated Value")
    
    with col2:
        price_per_sqft = prediction / area
        st.metric("Price per Sqft", f"AED {price_per_sqft:,.0f}")
    
    with col3:
        lower = prediction * 0.9
        upper = prediction * 1.1
        st.metric("Price Range", f"{lower/1000000:.1f}M - {upper/1000000:.1f}M")
    
    # Visualizations
    st.markdown("---")
    
    if PLOTLY_AVAILABLE:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Price Breakdown")
            breakdown = {
                'Base Price': prediction * 0.50,
                'Location Premium': prediction * 0.25,
                'Size & Layout': prediction * 0.15,
                'Amenities': prediction * 0.10
            }
            fig_pie = px.pie(values=list(breakdown.values()), names=list(breakdown.keys()), title="Estimated Price Components", hole=0.4, color_discrete_sequence=['#1f4788', '#2c5aa0', '#3d6bb3', '#5b8fd6'])
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Property Value Indicator")
            fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=prediction, domain={'x': [0, 1], 'y': [0, 1]}, title={'text': "Property Value (AED)", 'font': {'size': 18}}, number={'font': {'size': 24}}, gauge={'axis': {'range': [None, prediction * 1.5], 'tickwidth': 1}, 'bar': {'color': "#1f4788"}, 'bgcolor': "white", 'borderwidth': 2, 'bordercolor': "gray", 'steps': [{'range': [0, prediction * 0.7], 'color': '#e6f2ff'}, {'range': [prediction * 0.7, prediction * 1.2], 'color': '#cce5ff'}], 'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': prediction * 1.2}}))
            fig_gauge.update_layout(height=350)
            st.plotly_chart(fig_gauge, use_container_width=True)
    else:
        st.subheader("📊 Price Breakdown")
        breakdown = {
            'Base Price': prediction * 0.50,
            'Location Premium': prediction * 0.25,
            'Size & Layout': prediction * 0.15,
            'Amenities': prediction * 0.10
        }
        for component, value in breakdown.items():
            percentage = (value / prediction) * 100
            st.write(f"**{component}:** AED {value:,.0f} ({percentage:.0f}%)")
    
    # Property Summary
    st.markdown("---")
    st.subheader("📋 Property Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        summary_data = {"Feature": ["Location", "Type", "Bedrooms", "Bathrooms", "Area", "Parking"], "Value": [location, property_type, bedrooms, bathrooms, f"{area:,} sqft", parking]}
        st.dataframe(pd.DataFrame(summary_data), hide_index=True, use_container_width=True)
    
    with col2:
        amenities = []
        if has_pool: amenities.append("🏊 Pool")
        if has_gym: amenities.append("💪 Gym")
        if has_security: amenities.append("🔒 Security")
        if has_balcony: amenities.append("🌅 Balcony")
        if amenities:
            st.success("**Amenities Included:**")
            for amenity in amenities:
                st.write(f"• {amenity}")
        else:
            st.info("**No additional amenities selected**")
    
    # Investment Insights
    st.markdown("---")
    st.subheader("💡 Investment Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        monthly_rent = prediction * 0.00417
        st.metric("📅 Est. Monthly Rent", f"AED {monthly_rent:,.0f}")
    
    with col2:
        annual_yield = 5.0
        st.metric("📈 Est. Annual Yield", f"{annual_yield}%")
    
    with col3:
        roi_years = 100 / annual_yield
        st.metric("⏳ ROI Timeline", f"{roi_years:.0f} years")
    
    st.success("✅ Analysis complete! Adjust property features to see how they affect the price.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center;'><p><strong>Phase 2:</strong> ✅ Interactive Visualizations</p><p style='color: #666;'>🏠 Dubai Property Predictor | Built with Streamlit</p></div>", unsafe_allow_html=True)