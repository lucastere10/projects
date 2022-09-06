import pandas as pd

nasdaq = pd.read_csv('Python Projects\\Dash\\Dash Finance App\\data\\nasdaq.csv')

print(nasdaq.head())

test = 'Armada Acquisition Corp. I Warrant'

#print(str(nasdaq['Symbol'][nasdaq['Name'] == test]))
print(nasdaq['Country'].unique())

