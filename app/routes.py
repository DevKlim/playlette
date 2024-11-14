from app import app
from flask import request, jsonify
import torch
from models.color_model import ColorModel

# Load the trained model
model = ColorModel(input_dim=3, output_dim=1)
model.load_state_dict(torch.load('models/color_model.pt'))
model.eval()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = torch.FloatTensor([data['features']])
    with torch.no_grad():
        prediction = model(features).item()
    # Convert prediction to a color (e.g., grayscale)
    color_value = int(prediction * 255)
    hex_color = '#{:02x}{:02x}{:02x}'.format(color_value, color_value, color_value)
    return jsonify({'color': hex_color})

feedback_data = []

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    feedback_data.append(data)
    # Optionally, save to a file or database
    return jsonify({'message': 'Feedback received'})