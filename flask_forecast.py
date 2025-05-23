from flask import Flask, render_template, request
from models.model_runner import run_forecast

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forecast', methods=['POST'])
def forecast():
    file = request.files['datafile']
    df_forecast, plot_path = run_forecast(file)
    return render_template('forecast.html', plot_url=plot_path)



if __name__ == '__main__':
    app.run(debug=True)