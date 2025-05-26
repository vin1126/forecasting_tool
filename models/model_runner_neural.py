import pandas as pd
from neuralprophet import NeuralProphet
import matplotlib.pyplot as plt
import os

def run_neural_forecast(file_storage):
    df = pd.read_csv(file_storage)
    dfh = df.copy()

    df = df[['Date', 'Volume']]
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)

    split_date = '1-Jan-2023'
    df_train = df.loc[df.index <= split_date].copy()
    df_test = df.loc[df.index > split_date].copy()

    df_train_nprophet = df_train.reset_index().rename(columns={'Date': 'ds', 'Volume': 'y'})
    df_test_nprophet = df_test.reset_index().rename(columns={'Date': 'ds', 'Volume': 'y'})

    # Holidays (as events)
    dfh['holiday'] = dfh['ImpactTag']
    holiday_df = dfh[['Date', 'holiday']]
    holiday_df = holiday_df.dropna()
    holiday_df = holiday_df[holiday_df['holiday'].str.contains('Holiday')]
    holiday_df = holiday_df.rename(columns={'Date': 'ds', 'holiday': 'event'})

    # Create NeuralProphet model
    model = NeuralProphet()

    if not holiday_df.empty:
        
        unique_holidays = holiday_df['event'].unique()
        for event in unique_holidays:
            model.add_events([event])
        df_train_nprophet = model.create_df_with_events(df_train_nprophet, events_df=holiday_df)

    # Fit and forecast
    model.fit(df_train_nprophet, freq='D')

    future = model.make_future_dataframe(df_train_nprophet, periods=len(df_test_nprophet), n_historic_predictions=True)

    if not holiday_df.empty:
        future = model.create_df_with_events(future, events_df=holiday_df)

    forecast = model.predict(future)

    # Plotting
    fig = model.plot(forecast)
    plot_path = 'static/neural_forecast.png'
    fig.savefig(plot_path)
    plt.close(fig)

    return forecast, plot_path
