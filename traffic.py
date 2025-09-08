import pandas as pd
import numpy as np

#reading a file
url_2023 = (r"C:\Users\user\PycharmProjects\data-analytics\input data\202306\202306\Flights_20230601_20230630.csv\Flights_202306.csv")
file = pd.read_csv(url_2023)

#cleaning
file.info()
x = file.isnull().sum()
y = file.isnull().sum().sum()
replace_null = file.fillna(np.nan)
drop_null = file.dropna(how='any')

