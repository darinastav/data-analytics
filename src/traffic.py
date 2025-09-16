import zipfile
import pandas as pd
import numpy as np
from traffic_functions import average_number_per_day, busiest_day, max_flights

# define input file inside archive
zip_file_name = "../data/input/flights.zip"
csv_file_name_2023 = "Flights_202306.csv"
csv_file_name_2022 = "Flights_202206.csv"



# reading archive
with zipfile.ZipFile(zip_file_name, 'r') as zip_file:
    # unzipping a file from archive
    with zip_file.open(csv_file_name_2023) as csv_file:
        # reading csv file
        file_2023 = pd.read_csv(csv_file)
    with zip_file.open(csv_file_name_2022) as csv_file:
        file_2022 = pd.read_csv(csv_file)

#cleaning
#file_2023.info()
x = file_2023.isnull().sum()
y = file_2022.isnull().sum()
file_2023.duplicated().sum()
file_2023['Date'] = pd.to_datetime(file_2023['ACTUAL OFF BLOCK TIME'], dayfirst=True, errors='coerce') #convert actual off block time from str to date
file_2023['Date Filed'] = pd.to_datetime(file_2023['FILED OFF BLOCK TIME'], dayfirst=True, errors='coerce') #convert filed off block time from str to date
file_2023 = file_2023[~file_2023['Date'].dt.date.isin(
    [pd.to_datetime("2023-07-01").date(),
     pd.to_datetime("2023-05-31").date()])] #to remove May and July from a loop 2023

file_2022['Date'] = pd.to_datetime(file_2022['ACTUAL OFF BLOCK TIME'], dayfirst=True, errors='coerce') #do the same as above but for 2022 year
file_2022['Date Filed'] = pd.to_datetime(file_2022['FILED OFF BLOCK TIME'], dayfirst=True, errors='coerce')
file_2022 = file_2022[~file_2022['Date'].dt.date.isin(
    [pd.to_datetime("2022-07-01").date(),
     pd.to_datetime("2022-05-31").date()])]

#EDA(Exploratory Data Analysis)
#traffic
total_flights_2023 = file_2023.shape[0]
total_flights_2022 = file_2022.shape[0]
pct_change = ((total_flights_2023 - total_flights_2022)/total_flights_2022)*100
print(f'The total amount of flights is: {total_flights_2023}')
print(f'The percentage change in 2023 comparing to 2022: {pct_change:.0f}%')

print(f'The average number flights per day in 2022 is: {average_number_per_day(file_2022):.0f}')
print(f'The average number flights per day in 2023 is: {average_number_per_day(file_2023):.0f}')
print(f'The busiest day in June 2022 is: {busiest_day(file_2022).date()} with {max_flights(file_2022)} flights')
print(f'The busiest day in June 2023 is: {busiest_day(file_2023).date()} with {max_flights(file_2023)} flights')

weekly_flights = file_2023.groupby(pd.Grouper(key='Date', freq='W-MON')).size().reset_index(name='Flights')
max_week = weekly_flights.loc[weekly_flights['Flights'].idxmax(), 'Date']
max_week_flights = weekly_flights.loc[weekly_flights['Flights'].idxmax(), 'Flights']
print(f'The busiest week was {max_week.date()} with {max_week_flights} flights')

#ATFCM delays
file_2023['Actual_minutes'] = file_2023['Date'].dt.hour * 60 + file_2023['Date'].dt.minute #extract hours and minutes from datetime
file_2023['Filed_minutes']  = file_2023['Date Filed'].dt.hour * 60 + file_2023['Date Filed'].dt.minute
file_2023['Delay'] = file_2023['Actual_minutes'] - file_2023['Filed_minutes']

file_2023['Delay'] = np.where(file_2023['Delay'] < 0,
                              file_2023['Delay'] + 24*60,
                              file_2023['Delay']) #to cal when arrival is after the midnight
total_delay_2023 = file_2023['Delay'].sum() #cal total delay in minutes
average_delay_2023 = file_2023['Delay'].mean()

print(f'The total delay in 2023 is: {total_delay_2023} minutes')
print(f'The average delay is: {average_delay_2023:.3f} minutes')

file_2022['Actual_minutes'] = file_2022['Date'].dt.hour * 60 + file_2022['Date'].dt.minute #extract hours and minutes from datetime
file_2022['Filed_minutes']  = file_2022['Date Filed'].dt.hour * 60 + file_2022['Date Filed'].dt.minute
file_2022['Delay'] = file_2022['Actual_minutes'] - file_2022['Filed_minutes']

file_2022['Delay'] = np.where(file_2022['Delay'] < 0,
                              file_2022['Delay'] + 24*60,
                              file_2022['Delay']) #to cal when arrival is after the midnight
total_delay_2022 = file_2022['Delay'].sum() #cal total delay in minutes
average_delay_2022 = file_2022['Delay'].mean()
print(f'The total delay in 2022 is: {total_delay_2022} minutes')
print(f'The average delay is: {average_delay_2022:.3f} minutes')

pct_delay_change = ((average_delay_2023 - average_delay_2022)/average_delay_2022)*100
print(f'The percentage change of delays in 2023 comparing to 2022 is: {pct_delay_change:.0f}% up')