import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import  iplot
import json

colors = json.load(open("data/crayola.json"))["data"]

covid_data = pd.read_csv("./data/covidImpact.csv")
#data_country = [country for country in covid_data.loc["COUNTRY"]]

print(covid_data.columns)

c_d_by_tc = covid_data.loc[:,["COUNTRY", "DATE", "TC"]]
c_d_by_tc["TC"] = c_d_by_tc["TC"].str.replace(",", ".")
c_d_by_tc["TC"]  = pd.to_numeric(c_d_by_tc["TC"])
top_c_by_tc = c_d_by_tc.groupby(["COUNTRY"]).sum().sort_values("TC", ascending=False)[:10]

print(type(top_c_by_tc.loc["COUNTRY",:]))



data = []
for i, country in enumerate(top_c_by_tc.loc[:, "COUNTRY"]):
    print(i, country)
    trace = go.Scatter(
                        x = c_d_by_tc.DATE,
                        y = c_d_by_tc.TC,
                        mode = "lines",
                        name = "total cases",
                        marker = dict(color = "rgb{0}".format(colors[i]["rgb"])),
                        text = country)
    data.append(trace)


    layout = dict(title = 'Cas Covid pour les 10 pays les plus touchés',
                  xaxis = dict(title = 'dates',ticklen = 5,zeroline= False)
    )
    fig = dict(data = data, layout = layout)
    iplot(fig)
