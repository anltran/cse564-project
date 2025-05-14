import pandas as pd

features = ['BORO_NM', 'CMPLNT_FR_DT', 'CMPLNT_FR_TM', 'LAW_CAT_CD', 'OFNS_DESC', 'PREM_TYP_DESC', 'Latitude', 'Longitude']

# Load the dataset
df = pd.read_csv('nypd-complaints-2021-2024.csv', usecols=features)
df = df.dropna()

df = df.sample(n=80000, replace=False, random_state=42)

# Identify rows with any zero and drop them
rows_with_zeros = (df == 0).any(axis=1)
df = df[~rows_with_zeros]

# Drop rows with any null values in BORO_NM
df = df[df.BORO_NM.isin(['MANHATTAN','QUEENS','BROOKLYN','BRONX','STATEN ISLAND'])]

# Convert the 'date' column to datetime objects
df['CMPLNT_FR_DT'] = pd.to_datetime(df['CMPLNT_FR_DT'], errors='coerce')
# df['CMPLNT_FR_TM'] = pd.to_datetime(df['CMPLNT_FR_TM'], format='%H:%M:%S', errors='coerce').dt.time
# df['timestamp'] = df.apply(lambda row: pd.Timestamp.combine(row['CMPLNT_FR_DT'], row['CMPLNT_FR_TM']), axis=1)
df = df.dropna()

# Extract year, month, day, day of week, and hour from the date and time columns
df['year'] = df['CMPLNT_FR_DT'].dt.year.astype(int)
df['month'] = df['CMPLNT_FR_DT'].dt.month.astype(int)
df['day'] = df['CMPLNT_FR_DT'].dt.day.astype(int)
df['day_of_week'] = df['CMPLNT_FR_DT'].dt.weekday
df['hour'] = df['CMPLNT_FR_TM'].str[:2].astype(int)

# Assign offense categories based on OFNS_DESC
theft = ['PETIT LARCENY', 'GRAND LARCENY', 'OTHER OFFENSES RELATED TO THEFT', 'ROBBERY', 'BURGLARY', 'GRAND LARCENY OF MOTOR VEHICLE', 'POSSESSION OF STOLEN PROPERTY', 'BURGLAR\'S TOOLS', 'PETIT LARCENY OF MOTOR VEHICLE']
disorder = ['HARRASSMENT 2', 'CRIMINAL MISCHIEF & RELATED OF', 'OFF. AGNST PUB ORD SENSBLTY &', 'OFFENSES AGAINST PUBLIC SAFETY', 'DISORDERLY CONDUCT', 'FORGERY', 'CRIMINAL TRESPASS', 'ARSON', 'GAMBLING']
violent = ['ASSAULT 3 & RELATED OFFENSES', 'FELONY ASSAULT', 'HOMICIDE-NEGLIGENT,UNCLASSIFIE', 'MURDER & NON-NEGL. MANSLAUGHTER', 'KIDNAPPING & RELATED OFFENSES']
traffic = ['VEHICLE AND TRAFFIC LAWS', 'INTOXICATED & IMPAIRED DRIVING', 'UNAUTHORIZED USE OF A VEHICLE', 'INTOXICATED/IMPAIRED DRIVING']
possession = ['DANGEROUS DRUGS', 'DANGEROUS WEAPONS', 'CANNABIS RELATED OFFENSES', 'UNLAWFUL POSS. WEAP. ON SCHOOL']
sexual = ['SEX CRIMES', 'RAPE', 'PROSTITUTION & RELATED OFFENSES']

def assign_offense(row):
    description = row['OFNS_DESC']
    if description in theft:
        return 'Theft'
    elif description in disorder or 'FRAUD' in description:
        return 'Disorderly Conduct'
    elif description in violent:
        return 'Violent Crime'
    elif description in traffic:
        return 'Traffic Violation/DUI'
    elif description in possession:
        return 'Drug/Weapon Possession'
    elif description in sexual:
        return 'Sexual Violence'
    else:
        return 'Other'
    
df['Offense Type'] = df.apply(assign_offense, axis=1)

# Assign location categories based on PREM_TYP_DESC
street = ['STREET', 'PARKING LOT/GARAGE (PUBLIC)', 'PARKING LOT/GARAGE (PRIVATE)', 'HIGHWAY/PARKWAY']
residential = ['HOTEL/MOTEL', 'HOMELESS SHELTER']
store = ['GROCERY/BODEGA', 'CLOTHING/BOUTIQUE', 'FOOD SUPERMARKET', 'GYM/FITNESS FACILITY', 'BANK', 'SMALL MERCHANT', 'BEAUTY & NAIL SALON', 'GAS STATION', 'JEWELRY', 'DRY CLEANER/LAUNDRY']
dining = ['RESTAURANT/DINER', 'BAR/NIGHT CLUB', 'FAST FOOD']
service = ['HOSPITAL', 'PARK/PLAYGROUND', 'PUBLIC BUILDING', 'COLLEGE/UNIVERSITY', 'CHURCH', 'SYNAGOGUE', 'MOSQUE']

def check_substring(string, substrings):
    return any(sub in string for sub in substrings)

def assign_location(row):
    loc = row['PREM_TYP_DESC']
    if loc in street:
        return 'Street and Roadway'
    elif loc in residential or check_substring(loc, ['RESIDENCE', 'APT', 'HOUS']):
        return 'Residential'
    elif check_substring(loc, ['TRANSIT', 'BUS', 'TAXI', 'TERMINAL']):
        return 'Public Transit'
    elif loc in store or 'STORE' in loc:
        return 'Store and Private Business'
    elif loc in dining:
        return 'Dining'
    elif loc in service or 'SCHOOL' in loc:
        return 'Public Service'
    else:
        return 'Other'
    
df['Location'] = df.apply(assign_location, axis=1)

df.rename(columns={'CMPLNT_FR_DT': 'Date', 'BORO_NM': 'Borough Name', 'LAW_CAT_CD': 'Level of Offense'}, inplace=True)

print(df.value_counts('year'))

# df.drop(columns=['CMPLNT_FR_DT', 'CMPLNT_FR_TM', 'OFNS_DESC', 'PREM_TYP_DESC'], inplace=True)

# Export the cleaned DataFrame to a CSV file
df.to_csv('data.csv', index=False)
