import pandas as pd

features = ['BORO_NM', 'CMPLNT_FR_DT', 'CMPLNT_FR_TM', 'LAW_CAT_CD', 'OFNS_DESC', 'PREM_TYP_DESC', 'Latitude', 'Longitude']

# Load the dataset
df = pd.read_csv('nypd-complaints.csv', usecols=features)
df = df.dropna()

# Identify rows with any zero and drop them
rows_with_zeros = (df == 0).any(axis=1)
df = df[~rows_with_zeros]

# Drop rows with any null values in BORO_NM
df = df[df.BORO_NM.isin(['MANHATTAN','QUEENS','BROOKLYN','BRONX','STATEN ISLAND'])]

# Convert the 'date' column to datetime objects
df['CMPLNT_FR_DT'] = pd.to_datetime(df['CMPLNT_FR_DT'], errors='coerce')
df = df.dropna()

# Extract year, month, and day
df['year'] = df['CMPLNT_FR_DT'].dt.year.astype(int)
df['month'] = df['CMPLNT_FR_DT'].dt.month.astype(int)
df['day'] = df['CMPLNT_FR_DT'].dt.day.astype(int)
df['day_of_week'] = df['CMPLNT_FR_DT'].dt.day_name()

# temp = df['PREM_TYP_DESC'].value_counts()
# print(temp)

# Export the cleaned DataFrame to a CSV file
df.to_csv('./data.csv', index=False)