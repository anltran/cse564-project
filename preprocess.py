import pandas as pd

features = ['BORO_NM', 'Longitude', 'Latitude', 'LAW_CAT_CD']

# Load the dataset
df = pd.read_csv('nypd-complaints.csv', usecols=features)

# Identify rows with any zero and drop them
rows_with_zeros = (df == 0).any(axis=1)
df = df[~rows_with_zeros]

# Drop rows with any null values in BORO_NM
df = df[df.BORO_NM.isin(['MANHATTAN','QUEENS','BROOKLYN','BRONX','STATEN ISLAND'])]

# Export the cleaned DataFrame to a CSV file
df.to_csv('./data.csv', index=False)