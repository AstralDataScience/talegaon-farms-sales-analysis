import pandas as pd
import glob
files = glob.glob("C:\\Users\\ACC1\\Desktop\\Project\\Big_Project\\*.xlsx")
df_list = []
for file in files:
    df =pd.read_excel(file)
    df_list.append(df)
    df = pd.concat(df_list,ignore_index=True)
df = df.drop(columns = ['Mobile'])
df.to_csv('talegaon_clean.csv',index=False)
print(df.shape)
print(df.dtypes)
print(df.head())
#check Missing values
print('Missing Values')
print(df.isnull().sum())
# Duplicate Values
print("\nDuplicate rows:",df.duplicated().sum())
# Date Range
print("\n Date Range:")
print("From:",df['Date'].min())
print("To:",df['Date'].max())
#Unqiue Categories
print("\n Unique Categoreis:",df['Category'].nunique())
print('Categoreis:', df['Category'].unique())

print("\n Unique product:",df['Product'].nunique())

print("\nOrder Total stats:")
print(df['Order_Total'].describe())

print(df[df['Tower'].isnull()]['Building'].value_counts())

df = df.drop(columns=['Tower'])
df = df.drop(columns=['Flat','Name'])

df = df[df['Category']!='Sample']

df = df[df['Order_Total']>0]

df = df.dropna(subset=['Order_Total'])
print(df.shape)
print(df.isnull().sum())

df = df.dropna(subset=['Building', 'Customer_ID'])
print(df.shape)
print(df.isnull().sum())

df.to_csv('talegaon_final_clean_csv',index=False)
print('Saved successfully')