from kg.EB_classes import load_json
import pandas as pd
import numpy as np

dbpedia_train = load_json("data/smarttask_dbpedia_train")

df = pd.DataFrame(dbpedia_train)


def flat(val):
    v = np.asarray(val)
    v2 = v.flatten()
    return str(v2)


df['flat list'] = df['type'].apply(flat)
df['test'] = df['flat list'].str.contains('Brewery')
df2 = df[df['test'] == True]

df2.to_csv('data/query.csv')
