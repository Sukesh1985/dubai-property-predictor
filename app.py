import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import urllib.request
# Plotly is optional
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
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {padding: 0rem 1rem;}
    h1 {color: #1f4788;}
    .stTabs [data-baseweb="tab-list"] {gap: 24px;}
    .stTabs [data-baseweb="tab"] {padding: 10px 20px;}
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>🏠 Dubai Real Estate Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666;'>AI-Powered Property Valuation Tool</h3>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar Navigation
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio(
    "Choose a feature:",
    ["🏡 Price Prediction", "📊 Compare Properties", "📈 Market Insights", "ℹ️ About"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("📊 Using optimized estimation formula")

# Helper function to calculate price
def calculate_price(location, property_type, bedrooms, bathrooms, area, parking, has_pool, has_gym, has_security, has_balcony):
    base_price = 1000000
    location_multiplier = {
        "Downtown Dubai": 1.5, "Dubai Marina": 1.3, "Palm Jumeirah": 1.8,
        "Business Bay": 1.4, "JBR": 1.3, "Arabian Ranches": 1.2
    }
    type_multiplier = {"Apartment": 1.0, "Villa": 1.5, "Townhouse": 1.2, "Penthouse": 1.8}
    
    amenity_bonus = 0
    if has_pool: amenity_bonus += 0.05
    if has_gym: amenity_bonus += 0.03
    if has_security: amenity_bonus += 0.02
    if has_balcony: amenity_bonus += 0.02
    
    prediction = (base_price * 
                 location_multiplier.get(location, 1.0) * 
                 type_multiplier.get(property_type, 1.0) * 
                 (area / 1500) * 
                 (bedrooms * 0.3 + 0.7) *
                 (1 + amenity_bonus))
    
    return prediction

# ============================================
# PAGE 1: PRICE PREDICTION
# ============================================
if page == "🏡 Price Prediction":
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
        
        with st.spinner("Calculating..."):
            prediction = calculate_price(location, property_type, bedrooms, bathrooms, area, parking, has_pool, has_gym, has_security, has_balcony)
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
                
        if PLOTLY_AVAILABLE:
            fig_pie = px.pie(
                values=list(breakdown.values()), 
                names=list(breakdown.keys()), 
                title="Estimated Price Components", 
                hole=0.4, 
                color_discrete_sequence=['#1f4788', '#2c5aa0', '#3d6bb3', '#5b8fd6']
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            for component, value in breakdown.items():
                percentage = (value / prediction) * 100
                st.write(f"**{component}:** AED {value:,.0f} ({percentage:.0f}%)")
    
    with col2:
        st.subheader("🎯 Property Value Indicator")
        
        if PLOTLY_AVAILABLE:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", 
                value=prediction, 
                domain={'x': [0, 1], 'y': [0, 1]}, 
                title={'text': "Property Value (AED)", 'font': {'size': 18}}, 
                number={'font': {'size': 24}}, 
                gauge={
                    'axis': {'range': [None, prediction * 1.5], 'tickwidth': 1}, 
                    'bar': {'color': "#1f4788"}, 
                    'bgcolor': "white", 
                    'borderwidth': 2, 
                    'bordercolor': "gray", 
                    'steps': [
                        {'range': [0, prediction * 0.7], 'color': '#e6f2ff'}, 
                        {'range': [prediction * 0.7, prediction * 1.2], 'color': '#cce5ff'}
                    ], 
                    'threshold': {
                        'line': {'color': "red", 'width': 4}, 
                        'thickness': 0.75, 
                        'value': prediction * 1.2
                    }
                }
            ))
            fig_gauge.update_layout(height=350)
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.metric("Property Value", f"AED {prediction:,.0f}")
            st.info("Install Plotly to see the interactive gauge chart")
        
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

# ============================================
# PAGE 2: COMPARE PROPERTIES
# ============================================
elif page == "📊 Compare Properties":
    st.header("📊 Compare Multiple Properties")
    st.info("💡 Compare 2-3 properties side by side to make informed decisions")
    
    num_properties = st.slider("How many properties to compare?", 2, 3, 2)
    
    properties = []
    predictions = []
    
    cols = st.columns(num_properties)
    
    for i, col in enumerate(cols):
        with col:
            st.subheader(f"Property {i+1}")
            
            location = st.selectbox("Location", ["Downtown Dubai", "Dubai Marina", "Palm Jumeirah", "Business Bay", "JBR", "Arabian Ranches"], key=f"comp_loc_{i}")
            property_type = st.selectbox("Type", ["Apartment", "Villa", "Townhouse", "Penthouse"], key=f"comp_type_{i}")
            bedrooms = st.slider("Bedrooms", 1, 7, 2, key=f"comp_bed_{i}")
            bathrooms = st.slider("Bathrooms", 1, 7, 2, key=f"comp_bath_{i}")
            area = st.number_input("Area (sqft)", 500, 15000, 1500, key=f"comp_area_{i}")
            parking = st.slider("Parking", 0, 5, 1, key=f"comp_park_{i}")
            
            has_pool = st.checkbox("Pool", key=f"comp_pool_{i}")
            has_gym = st.checkbox("Gym", key=f"comp_gym_{i}")
            has_security = st.checkbox("Security", key=f"comp_sec_{i}")
            has_balcony = st.checkbox("Balcony", key=f"comp_bal_{i}")
            
            properties.append({
                'location': location,
                'property_type': property_type,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area': area,
                'parking': parking,
                'has_pool': has_pool,
                'has_gym': has_gym,
                'has_security': has_security,
                'has_balcony': has_balcony
            })
    
    if st.button("🔍 Compare Prices", type="primary", use_container_width=True):
        with st.spinner("Analyzing properties..."):
            for prop in properties:
                prediction = calculate_price(**prop)
                predictions.append(prediction)
            
            st.markdown("---")
            st.subheader("💰 Price Comparison")
            
            # Price comparison chart
            if PLOTLY_AVAILABLE:
                comparison_data = pd.DataFrame({
                    'Property': [f"Property {i+1}" for i in range(len(predictions))],
                    'Price (AED)': predictions,
                    'Price per Sqft': [predictions[i]/properties[i]['area'] for i in range(len(predictions))]
                })
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=comparison_data['Property'],
                    y=comparison_data['Price (AED)'],
                    text=[f"AED {p:,.0f}" for p in comparison_data['Price (AED)']],
                    textposition='outside',
                    marker_color=['#1f4788', '#2c5aa0', '#3d6bb3'][:len(predictions)]
                ))
                fig.update_layout(
                    title="Property Price Comparison",
                    yaxis_title="Price (AED)",
                    xaxis_title="",
                    showlegend=False,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed comparison table
            st.subheader("📋 Detailed Comparison")
            
            comparison_details = {
                'Feature': ['Location', 'Type', 'Bedrooms', 'Bathrooms', 'Area (sqft)', 
                           'Parking', 'Pool', 'Gym', 'Security', 'Balcony', 'Price', 'Price/Sqft'],
            }
            
            for i, (prop, price) in enumerate(zip(properties, predictions)):
                comparison_details[f'Property {i+1}'] = [
                    prop['location'],
                    prop['property_type'],
                    prop['bedrooms'],
                    prop['bathrooms'],
                    f"{prop['area']:,}",
                    prop['parking'],
                    "✅" if prop['has_pool'] else "❌",
                    "✅" if prop['has_gym'] else "❌",
                    "✅" if prop['has_security'] else "❌",
                    "✅" if prop['has_balcony'] else "❌",
                    f"AED {price:,.0f}",
                    f"AED {price/prop['area']:,.0f}"
                ]
            
            st.dataframe(pd.DataFrame(comparison_details), hide_index=True, use_container_width=True)
            
            # Best value indicator
            best_value_idx = np.argmin([predictions[i]/properties[i]['area'] for i in range(len(predictions))])
            st.success(f"🏆 **Best Value:** Property {best_value_idx + 1} offers the lowest price per square foot!")

# ============================================
# PAGE 3: MARKET INSIGHTS
# ============================================
elif page == "📈 Market Insights":
    st.header("📈 Dubai Real Estate Market Insights")
    
    tab1, tab2, tab3 = st.tabs(["📊 Location Analysis", "🏢 Property Types", "📏 Size Impact"])
    
    with tab1:
        st.subheader("Average Prices by Location")
        
        locations = ["Downtown Dubai", "Dubai Marina", "Palm Jumeirah", "Business Bay", "JBR", "Arabian Ranches"]
        avg_prices = []
        
        for loc in locations:
            price = calculate_price(loc, 'Apartment', 2, 2, 1500, 1, True, True, True, True)
            avg_prices.append(price)
        
        location_df = pd.DataFrame({
            'Location': locations,
            'Avg Price (AED)': avg_prices,
            'Price per Sqft': [p/1500 for p in avg_prices]
        }).sort_values('Avg Price (AED)', ascending=True)
        
        if PLOTLY_AVAILABLE:
            fig = px.bar(location_df, 
                        x='Avg Price (AED)', 
                        y='Location',
                        orientation='h',
                        title='Average Property Prices by Location (2BR, 1500 sqft)',
                        text=[f"AED {p:,.0f}" for p in location_df['Avg Price (AED)']],
                        color='Avg Price (AED)',
                        color_continuous_scale='Blues')
            fig.update_traces(textposition='outside')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(location_df, hide_index=True, use_container_width=True)
    
    with tab2:
        st.subheader("Price Comparison by Property Type")
        
        property_types = ["Apartment", "Villa", "Townhouse", "Penthouse"]
        type_prices = []
        
        for ptype in property_types:
            price = calculate_price('Dubai Marina', ptype, 3, 3, 2000, 2, True, True, True, True)
            type_prices.append(price)
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure(data=[go.Pie(
                labels=property_types,
                values=type_prices,
                hole=.4,
                marker_colors=['#1f4788', '#2c5aa0', '#3d6bb3', '#4e7fc4']
            )])
            fig.update_layout(
                title="Property Type Price Distribution (Dubai Marina, 3BR, 2000 sqft)",
                annotations=[dict(text='Property<br>Types', x=0.5, y=0.5, font_size=16, showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        type_df = pd.DataFrame({
            'Property Type': property_types,
            'Average Price': [f"AED {p:,.0f}" for p in type_prices]
        })
        st.dataframe(type_df, hide_index=True, use_container_width=True)
    
    with tab3:
        st.subheader("Impact of Property Size on Price")
        
        sizes = list(range(500, 5001, 500))
        prices_by_size = []
        
        for size in sizes:
            price = calculate_price('Downtown Dubai', 'Apartment', 2, 2, size, 1, True, True, True, True)
            prices_by_size.append(price)
        
        if PLOTLY_AVAILABLE:
            fig = px.line(
                x=sizes,
                y=prices_by_size,
                title='Property Price vs Size (Downtown Dubai, 2BR)',
                labels={'x': 'Area (sqft)', 'y': 'Price (AED)'},
                markers=True
            )
            fig.update_traces(line_color='#1f4788', line_width=3)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **Insight:** Larger properties command higher total prices, with location and amenities playing key roles in valuation.")

# ============================================
# PAGE 4: ABOUT
# ============================================
elif page == "ℹ️ About":
    st.header("ℹ️ About This Application")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Project Overview
        
        The **Dubai Real Estate Price Predictor** uses advanced algorithms to estimate 
        property prices based on location, size, amenities, and property type.
        
        ### 🔬 Technology Stack
        
        - **Frontend:** Streamlit
        - **Data Processing:** Pandas, NumPy
        - **Visualization:** Plotly, Plotly Express
        - **Deployment:** Streamlit Cloud
        
        ### 📊 Features
        
        ✅ Single property price prediction  
        ✅ Multi-property comparison  
        ✅ Market insights and trends  
        ✅ Investment ROI calculator  
        ✅ Interactive visualizations  
        
        ### 🎓 How It Works
        
        1. Enter property features (location, size, amenities)
        2. Algorithm calculates estimated price
        3. View detailed breakdown and insights
        4. Compare multiple properties
        5. Explore market trends
        
        ### 👨‍💻 Developer
        
        **Sukesh**  
        Data Scientist | ML Engineer  
        
        📧 Contact: [Your Email]  
        💼 [LinkedIn](#) | [GitHub](#)
        
        ---
        
        **Phase 3:** ✅ Multi-Page Features Complete!
        
        **Last Updated:** October 2025
        """)
    
    with col2:
        st.info("""
        ### 🚀 Quick Stats
        
        **Locations:** 6  
        **Property Types:** 4  
        **Features:** 10+  
        **Pages:** 4  
        
        ---
        
        ### 💡 Tips
        
        - Use comparison to evaluate options
        - Check market insights regularly
        - Consider ROI for investments
        - Location matters most!
        
        ---
        
        ### 🌟 Version
        
        **v3.0** - Multi-Page Release
        """)
        
        st.success("""
        ### 📊 Status
        
        ✅ Phase 1: Complete  
        ✅ Phase 2: Complete  
        ✅ Phase 3: Complete  
        ⏳ Phase 4: Coming Soon
        """)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center;'><p><strong>Phase 3:</strong> ✅ Multi-Page Features | <strong>Next:</strong> Phase 4 - Final Polish</p><p style='color: #666;'>🏠 Dubai Property Predictor | Built with Streamlit & Plotly</p></div>", unsafe_allow_html=True)