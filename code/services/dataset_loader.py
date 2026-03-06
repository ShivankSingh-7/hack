import pandas as pd

def load_dataset(path="samples.csv"):
    df = pd.read_csv(path)
    return df