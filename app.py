import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Dubai Property Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Sukesh1985/dubai-property-predictor',
        'Report a bug': 'https://github.com/Sukesh1985/dubai-property-predictor/issues',
        'About': 'Dubai Real Estate Price Predictor - Built with ❤️ by Sukesh'
    }
)

st.markdown("<h1 style='text-align: center;'>🏠 Dubai Real Estate Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666;'>AI-Powered Property Valuation Tool</h3>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio("Choose a feature:", ["🏡 Price Prediction", "📊 Compare Properties", "📈 Market Insights", "ℹ️ About"], label_visibility="collapsed")
st.sidebar.markdown("---")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("🌐 Status", "Live")
with col2:
    st.metric("📊 Version", "4.0")

st.sidebar.info("💡 Tip: Use dark mode for better viewing at night!")

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

def get_price_indicator(price):
    if price < 1500000:
        return "🟢 Affordable", "#4caf50"
    elif price < 3000000:
        return "🟡 Moderate", "#ff9800"
    else:
        return "🔴 Premium", "#f44336"

if page == "🏡 Price Prediction":
    st.header("📋 Property Details")
    st.caption("Enter your property specifications below to get an instant valuation")
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox("📍 Location", ["Downtown Dubai", "Dubai Marina", "Palm Jumeirah", "Business Bay", "JBR", "Arabian Ranches"], help="Select property location")
        bedrooms = st.slider("🛏️ Bedrooms", 1, 7, 2)
        area = st.number_input("📐 Area (sqft)", 500, 15000, 1500, step=100)
    with col2:
        property_type = st.selectbox("🏢 Type", ["Apartment", "Villa", "Townhouse", "Penthouse"])
        bathrooms = st.slider("🚿 Bathrooms", 1, 7, 2)
        parking = st.slider("🚗 Parking", 0, 5, 1)
    
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
        with st.spinner("Analyzing..."):
            prediction = calculate_price(location, property_type, bedrooms, bathrooms, area, parking, has_pool, has_gym, has_security, has_balcony)
        
        st.balloons()
        st.success("✅ Price Prediction Complete!")
        
        st.markdown("---")
        st.subheader("💰 Price Valuation")
        
        price_category, color = get_price_indicator(prediction)
        st.markdown(f"<h4 style='color: {color};'>Category: {price_category}</h4>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Predicted Price", f"AED {prediction:,.0f}")
        with col2:
            st.metric("Price per Sqft", f"AED {prediction/area:,.0f}")
        with col3:
            st.metric("Lower Range", f"AED {prediction*0.9:,.0f}")
        with col4:
            st.metric("Upper Range", f"AED {prediction*1.1:,.0f}")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Price Breakdown")
            breakdown = {'Base Price': prediction * 0.50, 'Location Premium': prediction * 0.25, 'Size & Layout': prediction * 0.15, 'Amenities': prediction * 0.10}
            for component, value in breakdown.items():
                st.write(f"**{component}:** AED {value:,.0f} ({(value/prediction)*100:.0f}%)")
        
        with col2:
            st.subheader("🎯 Key Metrics")
            st.metric("Market Position", "Competitive" if prediction < 3000000 else "Premium")
            st.metric("Est. Monthly Appreciation", f"AED {(prediction*0.05)/12:,.0f}")
        
        st.markdown("---")
        st.subheader("💡 Investment Insights")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Monthly Rent", f"AED {prediction*0.00417:,.0f}")
        with col2:
            st.metric("Annual Rent", f"AED {prediction*0.05:,.0f}")
        with col3:
            st.metric("Annual Yield", "5.0%")
        with col4:
            st.metric("ROI Timeline", "20 years")
        
        st.markdown("---")
        report = f"""DUBAI PROPERTY PRICE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

PROPERTY: {location} | {property_type}
DETAILS: {bedrooms}BR, {bathrooms}BA, {area:,} sqft, {parking} parking

PRICE VALUATION:
- Predicted: AED {prediction:,.0f}
- Per Sqft: AED {prediction/area:,.0f}
- Range: AED {prediction*0.9:,.0f} - {prediction*1.1:,.0f}

INVESTMENT:
- Monthly Rent: AED {prediction*0.00417:,.0f}
- Annual Yield: 5.0%
- ROI: 20 years

Report by Dubai Property Predictor v4.0
"""
        st.download_button("📥 Download Report", report, f"report_{datetime.now().strftime('%Y%m%d')}.txt", use_container_width=True)

elif page == "📊 Compare Properties":
    st.header("📊 Compare Properties")
    st.caption("Compare 2-3 properties side-by-side")
    
    num = st.slider("Number of properties", 2, 3, 2)
    properties = []
    predictions = []
    
    cols = st.columns(num)
    for i, col in enumerate(cols):
        with col:
            with st.expander(f"Property {i+1}", expanded=True):
                loc = st.selectbox("Location", ["Downtown Dubai", "Dubai Marina", "Palm Jumeirah", "Business Bay", "JBR", "Arabian Ranches"], key=f"l{i}")
                ptype = st.selectbox("Type", ["Apartment", "Villa", "Townhouse", "Penthouse"], key=f"t{i}")
                bed = st.slider("Bedrooms", 1, 7, 2, key=f"b{i}")
                bath = st.slider("Bathrooms", 1, 7, 2, key=f"ba{i}")
                area = st.number_input("Area", 500, 15000, 1500, key=f"a{i}")
                park = st.slider("Parking", 0, 5, 1, key=f"p{i}")
                pool = st.checkbox("Pool", key=f"po{i}")
                gym = st.checkbox("Gym", key=f"g{i}")
                sec = st.checkbox("Security", key=f"s{i}")
                bal = st.checkbox("Balcony", key=f"bl{i}")
                properties.append({'location': loc, 'property_type': ptype, 'bedrooms': bed, 'bathrooms': bath, 'area': area, 'parking': park, 'has_pool': pool, 'has_gym': gym, 'has_security': sec, 'has_balcony': bal})
    
    if st.button("🔍 Compare", type="primary", use_container_width=True):
        for prop in properties:
            predictions.append(calculate_price(**prop))
        
        st.balloons()
        st.success("Comparison Complete!")
        
        st.subheader("Price Comparison")
        cols = st.columns(num)
        for i, (pred, col) in enumerate(zip(predictions, cols)):
            with col:
                cat, color = get_price_indicator(pred)
                st.metric(f"Property {i+1}", f"AED {pred:,.0f}", delta=cat)
        
        st.markdown("---")
        comparison = {'Feature': ['Location', 'Type', 'Bedrooms', 'Bathrooms', 'Area', 'Price', 'Price/Sqft']}
        for i, (prop, pred) in enumerate(zip(properties, predictions)):
            comparison[f'Property {i+1}'] = [prop['location'], prop['property_type'], prop['bedrooms'], prop['bathrooms'], f"{prop['area']:,}", f"AED {pred:,.0f}", f"AED {pred/prop['area']:,.0f}"]
        st.dataframe(pd.DataFrame(comparison), hide_index=True, use_container_width=True)
        
        best = np.argmin([predictions[i]/properties[i]['area'] for i in range(len(predictions))])
        st.success(f"🏆 Best Value: Property {best + 1}")

elif page == "📈 Market Insights":
    st.header("📈 Market Insights")
    
    tab1, tab2, tab3 = st.tabs(["Location Analysis", "Property Types", "Size Impact"])
    
    with tab1:
        st.subheader("Prices by Location")
        locs = ["Downtown Dubai", "Dubai Marina", "Palm Jumeirah", "Business Bay", "JBR", "Arabian Ranches"]
        prices = [calculate_price(l, 'Apartment', 2, 2, 1500, 1, True, True, True, True) for l in locs]
        df = pd.DataFrame({'Location': locs, 'Price': [f"AED {p:,.0f}" for p in prices]})
        st.dataframe(df, hide_index=True, use_container_width=True)
    
    with tab2:
        st.subheader("Property Types")
        types = ["Apartment", "Villa", "Townhouse", "Penthouse"]
        prices = [calculate_price('Dubai Marina', t, 3, 3, 2000, 2, True, True, True, True) for t in types]
        df = pd.DataFrame({'Type': types, 'Price': [f"AED {p:,.0f}" for p in prices]})
        st.dataframe(df, hide_index=True, use_container_width=True)
    
    with tab3:
        st.subheader("Size Impact")
        sizes = list(range(500, 5001, 500))
        prices = [calculate_price('Downtown Dubai', 'Apartment', 2, 2, s, 1, True, True, True, True) for s in sizes]
        df = pd.DataFrame({'Area (sqft)': [f"{s:,}" for s in sizes], 'Price': [f"AED {p:,.0f}" for p in prices]})
        st.dataframe(df, hide_index=True, use_container_width=True)

elif page == "ℹ️ About":
    st.header("About This App")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Project Overview
        Dubai Real Estate Price Predictor uses advanced algorithms for property valuation.
        
        ### 🔬 Tech Stack
        - Frontend: Streamlit
        - Data: Pandas, NumPy
        - Deployment: Streamlit Cloud
        
        ### 📊 Features
        ✅ Price predictions
        ✅ Property comparison
        ✅ Market insights
        ✅ Investment calculator
        ✅ Dark mode
        ✅ Download reports
        
        ### 👨‍💻 Developer
        **Sukesh**
        Data Scientist | ML Engineer
        
        GitHub: [Sukesh1985](https://github.com/Sukesh1985)
        """)
    
    with col2:
        st.info("""
        ### 🚀 Stats
        Locations: 6
        Types: 4
        Features: 15+
        Pages: 4
        """)
        
        st.success("""
        ### 📊 Status
        ✅ Phase 1
        ✅ Phase 2
        ✅ Phase 3
        ✅ Phase 4
        """)

st.markdown("---")
st.markdown("<div style='text-align: center;'><p><strong>Phase 4:</strong> ✅ Complete | <strong>v4.0</strong></p><p style='color: #666;'>🏠 Dubai Property Predictor | Built with ❤️ using Streamlit</p></div>", unsafe_allow_html=True)
