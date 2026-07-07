import pandas as pd
import numpy as np

# ndarray_data = np.array([
#     ['Google', 10],
#     ['Runoob', 12],
#     ['Wiki', 13]
# ])

# df = pd.DataFrame(ndarray_data, columns=['Site', 'Age'])
# df['Age'] = pd.to_numeric(df['Age'])
# # print(df.loc[1:2, 'Age'])
# # print(df.iloc[1:2])
# # print(df.Site)
# # print(df['Age'])
# # print(df.info())
# # print(df.describe())
# # df_rev_sorted = df.sort_values(by='Age', ascending=False)
# # print(df_rev_sorted)
# df = pd.concat([df, pd.DataFrame({'Site': ['Amazon', 'Microsoft'], 'Age': [20, 40]})], ignore_index=True)
# print(df)
# print(df['Age'].mean())
# print(df[df['Age']>20])

data = pd.read_csv('full_unique_workers_20260614.csv')
ages = 2026 - data['Birthday Year']
data['Phone'] = data['Phone'].astype(str).str.rstrip('.0')
data = pd.concat([data, pd.DataFrame({'Age': ages})], axis=1)
# print(data.nlargest(5, 'Age'))
# print(data['Age'].drop_duplicates().sort_values(ascending=False).iloc[1])
print(data[data['Work Experience'].str.contains('forklift', case=False)].loc[:, ('Name', 'Phone')])
print(f'male: {(data['Gender'] == 'male').sum()}')
print(f'female: {(data['Gender'] == 'female').sum()}')
print(f'other: {(~data['Gender'].isin(['male', 'female'])).sum()}')