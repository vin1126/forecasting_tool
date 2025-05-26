from flask import Flask, render_template, request
from models.model_runner import run_forecast
from models.model_runner_neural import run_neural_forecast
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forecast', methods=['POST'])
def forecast():
    file = request.files['datafile']
    model_type = request.form.get('model')

    if model_type == 'neural':
        df_forecast, plot_path = run_neural_forecast(file)
    else:
        df_forecast, plot_path = run_forecast(file)

    return render_template('forecast.html', plot_url=plot_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)