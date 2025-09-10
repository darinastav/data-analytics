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
        file = pd.read_csv(csv_file)

#cleaning
#file.info()
file.isnull().sum()
file.duplicated().sum()
convert_date = file['ACTUAL OFF BLOCK TIME'].str.split(' ', n=1, expand=True)[0]
file['Date'] = convert_date
drop_june = file[file['Date'] == '01-07-2023']
drop_may = file[file['Date'] == '31-05-2023']
x = file.drop(drop_june.index, inplace=True)
y = file.drop(drop_may.index, inplace=True)

#EDA(Exploratory Data Analysis)
total_flights = file.shape[0]
print(f'The total amount of flights is: {total_flights}')

daily_flights = file.groupby('Date').size().reset_index(name='Flights') #counts flights per day
average_flights_per_day = daily_flights['Flights'].mean()
print(f'The average number flights per day is: {average_flights_per_day:.0f}')

busiest_day = daily_flights.loc[daily_flights['Flights'].idxmax(), 'Date']
max_flights = daily_flights.loc[daily_flights['Flights'].idxmax(), 'Flights']
print(f'The busiest day in June 2023 is: {busiest_day} with {max_flights} flights')
