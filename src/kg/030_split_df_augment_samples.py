''' import csv, split into types/categories, select randomly from training data to train classifier'''

import pandas as pd
import pickle
import random
import numpy as np
from ontology.onto_access import DBpediaOntology
from owlready2 import *

# read csv file
df = pd.read_csv('data/df.csv')

print('done read from csv')
#
# # check for missing values etc.
# df.isnull().sum()
#
# dict_of_types = dict(iter(df.groupby('type')))
# dict_of_categories = dict(iter(df.groupby('category')))
#
# print('done split to types and categories')
#
# '''test different strategies to augment positive and negative samples'''

# query for siblings of target types
# siblings of the classes associated with the target types e.g. ‘basketball player’ vs. ‘football player’
# uri_onto="http://www.cs.ox.ac.uk/isg/ontologies/schema.org.owl"
# onto_access = DBpediaOntology()
# onto_access.loadOntology(True)
#
#
# def get_sibling(type):
#     type2 = type.split('\'')
#     types = []
#     labels = []
#     for t in type2:
#         type3 = t.replace("[", "")
#         type4 = type3.replace(",", "")
#         type5 = type4.replace("]", "")
#         type6 = type5.replace(" ", "")
#         type7 = type6.replace("\n", "")
#         types.append(type7)
#     for t in types:
#         while "" in types:
#             types.remove("")
#         t2 = str(t.replace("dbo:", ""))
#         # print('t2', t2)
#         try:
#             # print("\n 1")
#             ancestors = onto_access.getAncestorsURIs(onto_access.getClassByName(t2))
#             # print('ancestors', ancestors)
#             ancestor = random.sample(ancestors, k=1)
#             # print('ancestor', ancestor[0])
#             cl8ss = onto_access.getClassByURI(ancestor[0])
#             siblings = onto_access.getDescendantNames(cl8ss)
#             # print('siblings', siblings)
#             sibling = random.sample(siblings, k=1)
#             # print('sibling', sibling[0])
#             while sibling[0] == t:
#                  sibling = random.sample(siblings, k=1)
#             labels.append(sibling[0])
#         except:
#             try:
#                 # print("\n 2")
#                 similar = onto_access.getClassIRIsContainingName(t2)
#                 labels = onto_access.getDescendantNames(similar)
#                 label = random.sample(labels, k=1)
#                 labels.append(label[0])
#                 # print(label[0])
#             except:
#                 pass
#     # print('\n types', types)
#     # print('labels', labels)
#     return labels
#
#
# df['sibling_type'] = df['type'].apply(get_sibling)   # column by column


# shuffle the answer categories and types independent of the questions to get a random answer category/type
def shuffle(df_column):
    df['output_column'] = df_column
    n_rows = len(df_column)
    pick_new_rows = np.random.permutation(list(range(n_rows)))[0:n_rows]
    # df.loc[pick_new_rows, 'output_column'] = np.random.permutation(df.loc[pick_new_rows, 'output_column'])
    shuffled_values = np.random.permutation(df['output_column'][pick_new_rows])
    df['output_column'][pick_new_rows] = shuffled_values
    return df


df2 = df['type'].apply(shuffle)
print('done shuffle')

df2.to_csv('data/df2.csv')
print('done read to csv')

# separate positive and negative samples
#
# # pickle
#
# f = open('data/positive_samples.pkl', 'rb')
# pickle.dump(positive_samples,f)
# f.close()
#
# f = open('data/negative_samples.pkl', 'rb')
# pickle.dump(negative_samples,f)
# f.close()
