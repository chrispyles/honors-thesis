import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")
import datetime as dt

def load_grafana_data(file):
    df = pd.read_csv(file)

    df["series"] = df.iloc[:,0].str.split(";").str[0]
    df["timestamp"] = df.iloc[:,0].str.split(";").str[1].str[1:-1]
    df["value"] = df.iloc[:,0].str.split(";").str[2]
    df = df[df["value"] != "null"]
    df["value"] = df["value"].astype(float)
    df = df.iloc[:,1:]
    return df
