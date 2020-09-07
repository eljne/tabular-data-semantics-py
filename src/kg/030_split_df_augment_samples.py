''' import csv, split into types/categories, select randomly from training data to train classifier'''

import pandas as pd
import pickle
import random
import numpy as np
from ontology.onto_access import DBpediaOntology

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
uri_onto = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/dbpedia_2014_fix.owl"
onto_access = DBpediaOntology()
onto_access.loadOntology(True)


def get_sibling(type):
    if type != "''":
        ancestors = onto_access.getDescendantNamesForClassName(type)
        # ancestors = onto_access.getClassByName(type).ancestors())
        # get ancestor
        ancestor = ancestors.pop()
        # siblings = onto_access.getDescendantNames(ancestor)
        siblings = onto_access.getClassByName(ancestor).descendants()
        sibling = siblings.pop()
        if sibling == type:
            sibling = siblings.pop()
    else:
        return ''
    return sibling


df['sibling_type'] = get_sibling(df['type'])


# also members of the same type e.g. different basketball players
# def get_member_sametype(type):
#
#     return member

# shuffle the answer categories and types independent of the questions to get a random answer category/type


def shuffle(df, df_column, output_column):
    n_rows = len(df_column)
    pick_new_rows = random.sample(range(1, n_rows), n_rows)
    df.loc[pick_new_rows, output_column] = np.random.permutation(df.loc[pick_new_rows, output_column])
    return df


df2 = shuffle(df, df['type'], 'shuffled_type')

# ep.getTopTypesUsingPredicatesForObject(ent, 3)





# pickle

f = open('data/positive_samples.pkl', 'rb')
pickle.dump(positive_samples,f)
f.close()

f = open('data/negative_samples.pkl', 'rb')
pickle.dump(negative_samples,f)
f.close()
