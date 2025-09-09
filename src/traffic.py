import zipfile
import pandas as pd
import numpy as np

# define input file inside archive
zip_file_name = "../data/input/Flights_202306.zip"
csv_file_name = "Flights_202306.csv"


# reading archive
with zipfile.ZipFile(zip_file_name, 'r') as zip_file:
    # unzipping a file from archive
    with zip_file.open(csv_file_name) as csv_file:
        # reading csv file
        file = pd.read_csv(csv_file)

#cleaning
file.info()
x = file.isnull().sum()
y = file.isnull().sum().sum()
replace_null = file.fillna(np.nan)
drop_null = file.dropna(how='any')

