from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
model1 = pickle.load(open('model1.pkl', 'rb'))

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

city_mapping = {
    'guntur': 26,
    'krishna': 27,
    'vijayawada': 28,
    'kurnool': 29,
    'godavari': 30
}

@app.route('/')
def home():
    return render_template('index.html', city_mapping=city_mapping, panel_mapping=panel_mapping)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        selected_panel_for_prediction = request.form['panel']
        selected_investment = float(request.form['investment'])
        selected_city_for_investment = request.form['investment_city']
        selected_city_for_prediction = request.form['panel_city']

        if 'predict_panel' in request.form:
            AM = float(panel_mapping[selected_panel_for_prediction])
            HD = float(city_mapping[selected_city_for_prediction])

            data = [[AM, HD]]
            result = model.predict(data)
            print("Shape of result:", result.shape)  # Add this line to check the shape of the result array
            result_dict = {
                'Surface Area': result[0],
                'Tilt': result[1],
                'Power': result[2]
            }
            return render_template('result.html', result=result_dict)

        if 'predict_investment' in request.form:
            INVESTMENT = float(selected_investment)
            HD = float(city_mapping[selected_city_for_investment])

            data = [[HD, INVESTMENT]]
            result = model1.predict(data)
            print("Shape of result:", result.shape)  # Add this line to check the shape of the result array
            result_dict = {
                'Surface Area': result[0],
                'Tilt': result[1],
                'Power': result[2]
            }
            return render_template('result.html', result=result_dict)

if __name__ == '__main__':
    app.run(debug=True)
