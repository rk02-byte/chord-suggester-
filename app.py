from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from lstm_model import predict_chords

app = Flask(__name__)
CORS(app)

# Load the pre-trained model
model = load_model("chord_predictor_model.h5")

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json.get('chords', [])
    if not data:
        return jsonify({"error": "No chords provided"}), 400
    try:
        suggested_chord, probability = predict_chords(model, data)
        return jsonify({"chord": suggested_chord, "probability": round(probability, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test_predict():
    try:
        test_chords = ["C", "G", "Am"]  # Simulated input
        suggested_chord, probability = predict_chords(model, test_chords)
        print(f"Test Suggestion: {suggested_chord}, Probability: {probability}")
        return jsonify({"chord": suggested_chord, "probability": probability})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
