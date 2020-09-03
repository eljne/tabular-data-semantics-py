''' import csv, split into types/categories, select randomly from training data to train classifier'''

import pandas as pd

# read csv file
df = pd.read_csv('data/df.csv')

# check for missing values etc.
df.isnull().sum()

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

def train_test(dataset, fraction):
    train_set = dataset.sample(frac=fraction, random_state=0)
    test_set = dataset.drop(train_set.index)
    return train_set, test_set

def train_classifier(train_set):
    return classifier

classifiers = {}

for category, df in dict_of_categories:
    train_set, test_set = train_test(df, 0.80)
    classifier = train_classifier(train_set)


for type in dict_of_types:
    train_set, test_set = train_test(df, 0.80)
    classifier = train_classifier(train_set)


'''test different strategies to augment positive and negative samples'''

# query for siblings of target types
# siblings of the classes associated with the target types e.g. ‘basketball player’ vs. ‘football player’
# also members of the same type e.g. different basketball players

# shuffle the answer categories and types independent of the questions to get a random answer category/type