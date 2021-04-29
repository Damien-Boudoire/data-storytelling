import pandas as pd

def load_covid():
    df = pd.read_csv("data/data_transformed.csv")
    df = df.set_index('date', drop = False)
    df = df.dropna()
    return df