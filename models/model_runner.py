import pandas as pd
from prophet import Prophet
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import cross_validation

import pandas as pd
import matplotlib.pyplot as plt
import os

def run_forecast(file_storage):
    df = pd.read_csv(file_storage)
    dfh = df.copy()

    df = df[['Date', 'Volume']]
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)

    split_date = '1-Jan-2023'
    df_train = df.loc[df.index <= split_date].copy()
    df_test = df.loc[df.index > split_date].copy()


    df_train_prophet = df_train.reset_index() \
        .rename(columns={'Date':'ds',
                        'Volume':'y'})
    
    df_test_prophet = df_test.reset_index() \
        .rename(columns={'Date':'ds',
                        'Volume':'y'})

    

    dfh['holiday'] = dfh['ImpactTag']

    holiday_df = dfh[['Date', 'holiday']]
    holiday_df = holiday_df.dropna()
    holiday_df = holiday_df[holiday_df['holiday'].str.contains('Holiday')]
    holiday_df = holiday_df.set_index('Date')
    holiday_df.index = pd.to_datetime(holiday_df.index)

    holiday_df = holiday_df.reset_index() \
        .rename(columns={'Date':'ds'})
    holiday_df


    model_with_holidays = Prophet(holidays=holiday_df)
    #model_with_holidays = Prophet(holidays=holiday_df)
    model_with_holidays.fit(df_train_prophet)



    forecast = model_with_holidays.predict(df_test_prophet)

    fig = model_with_holidays.plot(forecast)
    plot_path = 'static/forecast.png'
    plt.savefig(plot_path)
    plt.close()

    return forecast, plot_path
