from flask import Flask, jsonify
from flask_ngrok import run_with_ngrok
import stock-prediction-model-joblib.ipynb
import pandas as pd

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when the app is run

# Load the pre-trained model
model = joblib.load('stock_prediction_model.joblib')

@app.route('/predict', methods=['GET'])
def predict():
    # Fetch real-time data every 1 minute
    ticker = 'AAPL'
    data = yf.download(ticker, period='1d', interval='1m').tail(5)

    # Simulate trading
    future_data = pd.DataFrame(columns=['predicted'])
    for _ in range(5):
        next_time_point = data.tail(1)
        next_time_point.drop(columns=['Returns'], inplace=True)

        # Predict the next closing price
        predicted_price = model.predict(next_time_point[features])
        future_data = future_data.append({'predicted': predicted_price[0]}, ignore_index=True)

    return jsonify({'predictions': future_data.to_dict()})

if __name__ == '__main__':
    app.run()
