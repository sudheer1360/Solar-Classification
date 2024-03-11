import streamlit as st
import pickle

model = pickle.load(open('model.pkl', 'rb'))
model1 = pickle.load(open('model1.pkl', 'rb'))

st.title('Solar Classification ')

# Mapping of panel names to numerical values
panel_mapping = {
    'thin-film solar panel': 0,
    'hybrid solar panel': 1,
    'blue solar panel': 2,
    'monocrystalline solar panel': 3,
    'SMA - Sunny Boy 3300 TL': 4,
    'Fronius - IG 30': 5,
    'SMA - Sunny Boy 1700': 6,
    'Diehl AKO - Platinum 4800TL': 7,
    'CONERGY - WR 1700': 8,
    'Photowatt - PWI-6-30-I': 9,
    'SMA - Sunny Boy 2500': 10,
    'SMA - Sunny Boy 2100TL': 11,
    'AEG - Protect-PV 250': 12,
    'SMA - Sunny Boy 3000TL': 13,
    'Sputnik - SOLARMAX 3000S': 14,
    'SMA - Sunny Mini Central 8': 15,
    'Schuco - SGI-3000': 16,
    'Danfoss - UNILYNX 3600': 17,
    'Mastervolt - SunMaster XS3200': 18,
    'Tenesol - Connectis EI 3300': 19,
    'CONERGY - IPG3000': 20,
    'Fronius - IG 20': 21,
    'Sputnik - SOLARMAX SM3000S': 22,
    'Photowatt - PWI-6-40-I': 23,
    'SMA - Sunny Boy 3300': 24,
    'SMA - Sunny Boy 3000': 25
}

# Mapping of city names to numerical values
city_mapping = {
    'guntur': 26,
    'krishna': 27,
    'vijayawada': 28,
    'kurnool': 29,
    'godavari': 30
}

# Create dropdown for Investment
selected_investment = st.number_input('Enter the Investment:', min_value=0)

# Create dropdown for City
selected_city_for_investment = st.selectbox('Select the City for Investment:', list(city_mapping.keys()))

# Create dropdowns for Panel name and City for the main prediction
selected_panel_for_prediction = st.selectbox('Select the Panel name:', list(panel_mapping.keys()))
selected_city_for_prediction = st.selectbox('Select the City:', list(city_mapping.keys()))

if st.button('Predict based on Investment and City'):
    investment_value = float(selected_investment)
    city_value = city_mapping[selected_city_for_investment]

    data = [[city_value, investment_value]]
    result = model.predict(data)
    st.write('payback period: '+str(result[0][0]))
 

if st.button('Predict based on Panel and City'):
    panel_value = panel_mapping[selected_panel_for_prediction]
    city_value = city_mapping[selected_city_for_prediction]

    data = [[city_value, panel_value]]
    result = model1.predict(data)
    st.write('Surface Area: '+str(result[0][0]))
    st.write('Tilt: '+str(result[0][1]))
    st.write('Power: '+str(result[0][2]))
