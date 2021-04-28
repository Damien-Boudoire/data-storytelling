import numpy as np
import pandas as pd

df = pd.read_csv("data/data_transformed.csv")
df = df.set_index('date')
df = df.dropna()

df_countries = []
for p in np.unique(df.iso_code):
    df_countries.append(df[df['iso_code'] == p])

pop_ratio = {}
pop_totale = np.sum(np.unique(df.population))
for p in np.unique(df.location):
    pop_ratio[p] = round(df[df['location'] == p]['population'].mean()/pop_totale, 5)

df_concat_sti = df_countries[0].stringency_index
df_concat_tc = df_countries[0].total_cases
df_concat_td = df_countries[0].total_deaths
a = 0
for i in range(1, len(df_countries)):
    country = df_countries[i].location[0]
    df_concat_sti = pd.concat([df_concat_sti, df_countries[i].stringency_index], axis=1) * pop_ratio[country]
    df_concat_tc = pd.concat([df_concat_tc, df_countries[i].total_cases], axis=1)
    df_concat_td = pd.concat([df_concat_td, df_countries[i].total_deaths], axis=1)
    print(pop_ratio[country])
    print(df_countries[i].stringency_index.tail())
    print(df_concat_sti.iloc[-5:,-1])
    a += pop_ratio[country]
print(a)
df_concat_sti = df_concat_sti.fillna(method='ffill', axis = 0)
df_concat_tc = df_concat_tc.fillna(method='ffill', axis = 0)
df_concat_td = df_concat_td.fillna(method='ffill', axis = 0)

df_concat_sti.columns = np.unique(df.location)
a = df_concat_sti.sum(axis=1)
df_concat_sti['TOTAL'] = a
df_concat_sti.to_csv('sti.csv')

# df_world = pd.DataFrame({'date':df_concat_sti.index})
# df_world.index = df_concat_sti.index
# df_world['population'] = pop_totale
# df_world['iso_code'] = 'WORLD'
# df_world['location'] = 'Global'
# df_world['stringency_index'] = df_concat_sti.sum(axis=1)
# df_world['total_cases'] = df_concat_tc.sum(axis=1)
# df_world['total_deaths'] = df_concat_td.sum(axis=1)
# df_world.to_csv('test.csv')

