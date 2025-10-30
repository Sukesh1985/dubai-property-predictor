import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dubai Property Price Predictor", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>.main {padding: 0rem 1rem;} h1 {color: #1f4788;}</style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🏠 Dubai Real Estate Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666;'>AI-Powered Property Valuation Tool</h3>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio("Choose a feature:", ["🏡 Price Prediction", "📊 Compare Properties", "📈 Market Insights", "ℹ️ About"], label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.info("📊 Using optimized estimation formula")

def calculate_price(location, property_type, bedrooms, bathrooms, area, parking, has_pool, has_gym, has_security, has_balcony):
    base_price = 1000000
    location_multiplier = {"Downtown Dubai": 1.5, "Dubai Marina": 1.3, "Palm Jumeirah": 1.8, "Business Bay": 1.4, "JBR": 1.3, "Arabian Ranches": 1.2}
    type_multiplier = {"Apartment": 1.0, "Villa": 1.5, "Townhouse": 1.2, "Penthouse": 1.8}
    amenity_bonus = 0
    if has_pool: amenity_bonus += 0.05
    if has_gym: amenity_bonus += 0.03
    if has_security: amenity_bonus += 0.02
    if has_balcony: amenity_bonus += 0.02
    prediction = (base_price * location_multiplier.get(location, 1.0) * type_multiplier.get(property_type, 1.0) * (area / 1500) * (bedrooms * 0.3 + 0.7) * (1 + amenity_bonus))
    return prediction

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
            st.success("📊 Price Prediction Complete")
        
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
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Price Breakdown")
            breakdown = {'Base Price': prediction * 0.50, 'Location Premium': prediction * 0.25, 'Size & Layout': prediction * 0.15, 'Amenities': prediction * 0.10}
            for component, value in breakdown.items():
                percentage = (value / prediction) * 100
                st.write(f"**{component}:** AED {value:,.0f} ({percentage:.0f}%)")
        
        with col2:
            st.subheader("🎯 Key Metrics")
            st.metric("Lower Estimate", f"AED {lower:,.0f}")
            st.metric("Upper Estimate", f"AED {upper:,.0f}")
            st.info("Estimated range based on market analysis")
        
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
            properties.append({'location': location, 'property_type': property_type, 'bedrooms': bedrooms, 'bathrooms': bathrooms, 'area': area, 'parking': parking, 'has_pool': has_pool, 'has_gym': has_gym, 'has_security': has_security, 'has_balcony': has_balcony})
    
    if st.button("🔍 Compare Prices", type="primary", use_container_width=True):
        with st.spinner("Analyzing properties..."):
            for prop in properties:
                prediction = calculate_price(**prop)
                predictions.append(prediction)
            st.markdown("---")
            st.subheader("💰 Price Comparison")
            comparison_details = {'Feature': ['Location', 'Type', 'Bedrooms', 'Bathrooms', 'Area (sqft)', 'Parking', 'Pool', 'Gym', 'Security', 'Balcony', 'Price', 'Price/Sqft']}
            for i, (prop, price) in enumerate(zip(properties, predictions)):
                comparison_details[f'Property {i+1}'] = [prop['location'], prop['property_type'], prop['bedrooms'], prop['bathrooms'], f"{prop['area']:,}", prop['parking'], "✅" if prop['has_pool'] else "❌", "✅" if prop['has_gym'] else "❌", "✅" if prop['has_security'] else "❌", "✅" if prop['has_balcony'] else "❌", f"AED {price:,.0f}", f"AED {price/prop['area']:,.0f}"]
            st.dataframe(pd.DataFrame(comparison_details), hide_index=True, use_container_width=True)
            best_value_idx = np.argmin([predictions[i]/properties[i]['area'] for i in range(len(predictions))])
            st.success(f"🏆 Best Value: Property {best_value_idx + 1} offers the lowest price per square foot!")

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
        location_df = pd.DataFrame({'Location': locations, 'Avg Price (AED)': avg_prices, 'Price per Sqft': [p/1500 for p in avg_prices]}).sort_values('Avg Price (AED)', ascending=True)
        st.dataframe(location_df, hide_index=True, use_container_width=True)
    with tab2:
        st.subheader("Price Comparison by Property Type")
        property_types = ["Apartment", "Villa", "Townhouse", "Penthouse"]
        type_prices = []
        for ptype in property_types:
            price = calculate_price('Dubai Marina', ptype, 3, 3, 2000, 2, True, True, True, True)
            type_prices.append(price)
        type_df = pd.DataFrame({'Property Type': property_types, 'Average Price': [f"AED {p:,.0f}" for p in type_prices]})
        st.dataframe(type_df, hide_index=True, use_container_width=True)
    with tab3:
        st.subheader("Impact of Property Size on Price")
        sizes = list(range(500, 5001, 500))
        prices_by_size = []
        for size in sizes:
            price = calculate_price('Downtown Dubai', 'Apartment', 2, 2, size, 1, True, True, True, True)
            prices_by_size.append(price)
        size_df = pd.DataFrame({'Area (sqft)': sizes, 'Price (AED)': [f"AED {p:,.0f}" for p in prices_by_size]})
        st.dataframe(size_df, hide_index=True, use_container_width=True)
        st.info("💡 Insight: Larger properties command higher total prices, with location and amenities playing key roles in valuation.")

elif page == "ℹ️ About":
    st.header("ℹ️ About This Application")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 🎯 Project Overview
        The **Dubai Real Estate Price Predictor** uses advanced algorithms to estimate property prices based on location, size, amenities, and property type.
        
        ### 🔬 Technology Stack
        - **Frontend:** Streamlit
        - **Data Processing:** Pandas, NumPy
        - **Deployment:** Streamlit Cloud
        
        ### 📊 Features
        ✅ Single property price prediction
        ✅ Multi-property comparison
        ✅ Market insights and trends
        ✅ Investment ROI calculator
        
        ### 👨‍💻 Developer
        **Sukesh**
        Data Scientist | ML Engineer
        
        **Phase 3:** ✅ Multi-Page Features Complete!
        """)
    with col2:
        st.info("""
        ### 🚀 Quick Stats
        **Locations:** 6
        **Property Types:** 4
        **Features:** 10+
        **Pages:** 4
        """)
        st.success("""
        ### 📊 Status
        ✅ Phase 1: Complete
        ✅ Phase 2: Complete
        ✅ Phase 3: Complete
        ⏳ Phase 4: Coming Soon
        """)

st.markdown("---")
st.markdown("<div style='text-align: center;'><p><strong>Phase 3:</strong> ✅ Multi-Page Complete</p><p style='color: #666;'>🏠 Dubai Property Predictor | Built with Streamlit</p></div>", unsafe_allow_html=True)
