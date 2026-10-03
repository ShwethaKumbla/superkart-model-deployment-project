from flask import Flask, request, jsonify
import joblib
import pandas as pd
import io

superkart_api = Flask(__name__)

# Load the serialized model pipeline at startup
model = joblib.load('superkart_model.joblib')


@superkart_api.post('/v1/predict')
def predict():
    """Online inference: accepts a single JSON record and returns predicted sales."""
    data = request.get_json()
    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)[0]
    return jsonify({'predicted_sales': round(float(prediction), 2)})


@superkart_api.post('/v1/predictbatch')
def predict_batch():
    """Batch inference: accepts a CSV file and returns predictions for each row."""
    file = request.files.get('file')
    if file is None:
        return jsonify({'error': 'No file provided'}), 400
    df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    predictions = model.predict(df)
    result = {str(i): round(float(p), 2) for i, p in enumerate(predictions)}
    return jsonify(result)


if __name__ == '__main__':
    superkart_api.run(host='0.0.0.0', port=7860)
