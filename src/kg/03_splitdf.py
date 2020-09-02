''' import csv, split into types/categories, select randomly from training data to train classifier'''

import pandas as pd
import random

# read csv file
df = pd.read_csv('data/df.csv')

# find unique categories, types

# categories_list = ['boolean', 'literal', 'resource']
# temp = []
# for entry in dbpedia_train_wh:
#     ty = entry['type']
#     temp.append(ty)
# types_list = np.unique(temp)
#
# print('done found uniques')

dict_of_types = dict(iter(df.groupby('type')))
dict_of_categories = dict(iter(df.groupby('category')))

print('done split to types and categories')

'''select negative samples at random from training data'''
'''look at PDS coursework'''


