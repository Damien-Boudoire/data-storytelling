import pandas as pd

def load_covid():
    df = pd.read_csv("datasets/data_transformed.csv")
    df = df.set_index('date', drop = False)
    df = df.dropna()
    return df

def save_cases_and_deaths_on_pop(df):
    df['cases_pop'] = df['total_cases'] / df['population'] * 100
    df['deaths_pop'] = df['total_deaths'] / df['population'] * 100
