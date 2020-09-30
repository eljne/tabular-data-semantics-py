import pandas as pd
import json
from kg.EB_classes import unpickle

data = unpickle('training_vectors/32_all_td_justconcat')
df = pd.DataFrame(data)
print(df.head)