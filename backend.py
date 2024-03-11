from flask import Flask, render_template, request, jsonify, redirect, url_for
import pickle
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

app = Flask(__name__)

# Load your models for Solar Classification
model_solar = pickle.load(open('model.pkl', 'rb'))
model1_solar = pickle.load(open('model1.pkl', 'rb'))

# Load your models for Image Classification
model_image1 = load_model("keras_Model1.h5", compile=False)
model_image2 = load_model("keras_Model2.h5", compile=False)
model_image3 = load_model("keras_Model3.h5", compile=False)

class_names_image1 = open("labels1.txt", "r").readlines()
class_names_image2 = open("labels2.txt", "r").readlines()
class_names_image3 = open("labels3.txt", "r").readlines()

# Mapping of panel names to numerical values for Solar Classification
panel_mapping = {
    'thin-film solar panel': 0,
    'hybrid solar panel': 1,
    'blue solar panel': 2,
    'monocrystalline solar panel': 3,
    'SMA - Sunny Boy 3300 TL': 4,
    # Add more panel options here
}

# Mapping of city names to numerical values for Solar Classification
city_mapping = {
    'guntur': 26,
    'krishna': 27,
    'vijayawada': 28,
    'kurnool': 29,
    'godavari': 30
}

@app.route('/')
def index():
    return render_template('first.html')

@app.route('/predict_solar_investment', methods=['POST'])
def predict_solar_investment():
    try:
        print(request.json['investment'])
        investment = float(request.json['investment'])
        city = request.json['city']
        city_value = city_mapping[city]

        data = [[investment,city_value]]
        print(data)
        result = model_solar.predict(data)
        print(result)
        return jsonify({
            'payback_period': result[0][0]
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/solar_panel')
def solar_panel():
    return render_template('second.html')

@app.route('/no_solar_detected')
def no_solar_detected():
    return render_template('final.html')

@app.route('/predict_solar_panel', methods=['POST'])
def predict_solar_panel():
    try:
        panel = request.json['panel']
        city = request.json['city']
        panel_value = panel_mapping[panel]
        city_value = city_mapping[city]

        data = [[panel_value,city_value]]
        result = model1_solar.predict(data)
        return jsonify({
            'surface_area': result[0][0],
            'tilt': result[0][1],
            'power': result[0][2]
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/classify_image', methods=['POST'])
def classify_image():
    try:
        image = request.files['file']
        data = process_image(image)
        
        # Assuming class_names_image1 is appropriate for your use case
        # class_names = class_names_image1
        
        prediction1 = model_image1.predict(data)
        prediction2 = model_image2.predict(data)
        prediction3 = model_image3.predict(data)
        
        prediction1=list(prediction1[0])
        prediction2=list(prediction2[0])
        prediction3=list(prediction3[0])

        print(prediction1,max(prediction1))
        print(prediction2,max(prediction2))
        print(prediction3,max(prediction3))

        index1=prediction1.index(max(prediction1))
        index2=prediction2.index(max(prediction2))
        index3=prediction3.index(max(prediction3))
        
        print(index1)
        print(index2)
        print(index3)

        class_name1=class_names_image1[index1]
        confidence_score1=max(prediction1)
        confidence_score2=max(prediction2)
        class_name2=class_names_image2[index2]
        class_name3=class_names_image3[index3]
        confidence_score3=max(prediction3)
        # You might want to choose the class_name and confidence_score based on your logic
        
        return jsonify({'class_name1': class_name1, 'confidence_score1': str(confidence_score1),
                        'class_name2': class_name2, 'confidence_score2': str(confidence_score2),
                        'class_name3': class_name3, 'confidence_score3': str(confidence_score3)})
    except Exception as e:
        return jsonify({'error': str(e)})

def process_image(image):
    size = (224, 224)
    image = Image.open(image).convert("RGB")
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    return data

if __name__ == '__main__':
    app.run(port=5001,debug=True)
