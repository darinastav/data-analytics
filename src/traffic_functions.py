import pandas as pd

def average_number_per_day(data_frame):
    daily_flights = data_frame.groupby(pd.Grouper(key='Date', freq='D')).size().reset_index(name='Flights')
    return daily_flights['Flights'].mean()

def busiest_day(data_frame):
    daily_flights = data_frame.groupby(pd.Grouper(key='Date', freq='D')).size().reset_index(name='Flights')
    return daily_flights.loc[daily_flights['Flights'].idxmax(), 'Date']

def max_flights(data_frame):
    daily_flights = data_frame.groupby(pd.Grouper(key='Date', freq='D')).size().reset_index(name='Flights')
    return daily_flights.loc[daily_flights['Flights'].idxmax(), 'Flights']
