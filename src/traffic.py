import zipfile
import pandas as pd
import numpy as np

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
#file.info()
file_2023.isnull().sum()
file_2023.duplicated().sum()
#convert_date = file_2023['ACTUAL OFF BLOCK TIME'].str.split(' ', n=1, expand=True)[0]
#file_2023['Date'] = convert_date
#file_2023['Date'] = pd.to_datetime(file_2023['ACTUAL OFF BLOCK TIME'])
file_2023['Date'] = pd.to_datetime(file_2023['ACTUAL OFF BLOCK TIME'], format='%d-%m-%Y')
#file_2023['Date'] = pd.to_datetime(file_2023['Date'] )  # ensure datetime type
#file_2023['Date'] = pd.to_datetime(file_2023['ACTUAL OFF BLOCK TIME'], dayfirst=True, errors='coerce')
#print(file_2023['Date'])
drop_june = file_2023[file_2023['Date'] == '01-07-2023']
drop_may = file_2023[file_2023['Date'] == '31-05-2023']
x = file_2023.drop(drop_june.index, inplace=True)
y = file_2023.drop(drop_may.index, inplace=True)

#EDA(Exploratory Data Analysis)
total_flights_2023 = file_2023.shape[0]
total_flights_2022 = file_2022.shape[0]
pct_change = ((total_flights_2023 - total_flights_2022)/total_flights_2023)*100
print(f'The total amount of flights is: {total_flights_2023}')
print(f'The percentage change in 2023: {pct_change:.0f}%')

daily_flights = file_2023.groupby('Date').size().reset_index(name='Flights') #counts flights per day
average_flights_per_day = daily_flights['Flights'].mean()
print(f'The average number flights per day is: {average_flights_per_day:.0f}')

busiest_day = daily_flights.loc[daily_flights['Flights'].idxmax(), 'Date']
max_flights = daily_flights.loc[daily_flights['Flights'].idxmax(), 'Flights']
print(f'The busiest day in June 2023 is: {busiest_day} with {max_flights} flights')

weekly_flights = file_2023.groupby(pd.Grouper(key='Date', freq='W-MON')).size().reset_index(name='Flights')
print(weekly_flights)
