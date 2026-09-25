import pandas as pd

symbols = {'Š', '€', '„'}
total = 0

df1 = pd.read_csv('data1.csv', encoding='cp1252')
total += df1.loc[df1['symbol'].isin(symbols), 'value'].sum()

df2 = pd.read_csv('data2.csv', encoding='utf-8')
total += df2.loc[df2['symbol'].isin(symbols), 'value'].sum()

df3 = pd.read_csv('data3.txt', sep='\t', encoding='utf-16')
total += df3.loc[df3['symbol'].isin(symbols), 'value'].sum()

print(total)