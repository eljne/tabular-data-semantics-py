''' import csv, split into types/categories, select randomly from training data to train classifier'''

import pandas as pd
import pickle

# read csv file
df = pd.read_csv('data/df.csv')

print('done read from csv')

# check for missing values etc.
df.isnull().sum()

dict_of_types = dict(iter(df.groupby('type')))
dict_of_categories = dict(iter(df.groupby('category')))

print('done split to types and categories')

'''test different strategies to augment positive and negative samples'''

# query for siblings of target types
# siblings of the classes associated with the target types e.g. ‘basketball player’ vs. ‘football player’
# also members of the same type e.g. different basketball players

# shuffle the answer categories and types independent of the questions to get a random answer category/type










# pickle

f = open('data/positive_samples.pkl', 'rb')
pickle.dump(positive_samples,f)
f.close()

f = open('data/negative_samples.pkl', 'rb')
pickle.dump(negative_samples,f)
f.close()
