import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import  iplot
import json
colors = json.load(open("data/crayola.json"))["data"]

df = pd.read_csv("data/data_transformed.csv")
df = df.set_index('date')
df = df.dropna()
test = 0


df_countries = []
for p in np.unique(df.iso_code):
    df_countries.append(df[df['iso_code'] == p])

df_concat = df_countries[0].stringency_index
for i in range(1, len(df_countries)):
    df_concat = pd.concat([df_concat, df_countries[i].stringency_index], axis=1)
df_concat = df_concat.fillna(method='ffill', axis = 1)
df_concat.columns = np.unique(df.location)

a = df_concat.mean(axis=1)
df_concat['STI mean'] = a

df_concat.to_csv('test.csv')