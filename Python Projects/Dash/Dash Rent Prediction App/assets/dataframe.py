### --- DATAFRAME --- ###
#read df
df = pd.read_csv('data/House_Rent_Dataset.csv')
import pandas as pd
#transform to datetime
df['Posted On'] = pd.to_datetime(df['Posted On'])
#Unique Rented Floors
df['Floor'].str.split(' ').str[0].unique()
df['Rented Floor'] = df['Floor'].str.split(' ').str[0] #split and get 1st element
df['Build Size'] = df['Floor'].str.split(' ').str[-1] #split and get last element
#Rented Floor
df.loc[df['Rented Floor'] == 'Ground', 'Rented Floor'] = 1 #change 'Ground' value to 1
df.loc[df['Rented Floor'] == 'Upper', 'Rented Floor'] = df['Build Size'] #change 'Upper' value to last element
df.loc[df['Rented Floor'] == 'Lower', 'Rented Floor'] = 1 #change 'Lower' value to first element
#Build Size
df.loc[df['Build Size'] == 'Ground', 'Build Size'] = 1 #change 'Ground' value to 1
df['Rented Floor'] = df['Rented Floor'].astype(int)
df['Build Size'] = df['Build Size'].astype(int)
df['Floor'] = df[['Rented Floor','Build Size']].values.tolist() #change original floor values to a list tpye
#remove rent outlier
df = df[df['Rent'] < 1500000]
#remove Area Type with low values
df = df[df['Area Type'] != 'Built Area']