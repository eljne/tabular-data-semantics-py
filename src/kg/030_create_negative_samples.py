''' import csv, create negative samples from positive samples'''
# 9th september - ejb

import pandas as pd
import pickle
import random
import numpy as np
from ontology.onto_access import DBpediaOntology

# read csv file
df = pd.read_csv('data/df.csv')

print('done read from csv')

'''test different strategies to augment positive samples to get negative samples'''

# query for siblings of target types
# siblings of the classes associated with the target types e.g. ‘basketball player’ vs. ‘football player’
uri_onto = "http://www.cs.ox.ac.uk/isg/ontologies/schema.org.owl"
onto_access = DBpediaOntology()
onto_access.loadOntology(True)


def get_sibling(type):
    type2 = type.split('\'')
    types = []
    labels = []
    for t in type2:
        type3 = t.replace("[", "")
        type4 = type3.replace(",", "")
        type5 = type4.replace("]", "")
        type6 = type5.replace(" ", "")
        type7 = type6.replace("\n", "")
        types.append(type7)
    for t in types:
        while "" in types:
            types.remove("")
        t2 = str(t.replace("dbo:", ""))
        # print('t2', t2)
        try:
            # print("\n 1")
            ancestors = onto_access.getAncestorsURIs(onto_access.getClassByName(t2))
            # print('ancestors', ancestors)
            ancestor = random.sample(ancestors, k=1)
            # print('ancestor', ancestor[0])
            cl8ss = onto_access.getClassByURI(ancestor[0])
            siblings = onto_access.getDescendantNames(cl8ss)
            # print('siblings', siblings)
            sibling = random.sample(siblings, k=1)
            # print('sibling', sibling[0])
            while sibling[0] == t:
                 sibling = random.sample(siblings, k=1)
            labels.append(sibling[0])
        except:
            try:
                # print("\n 2")
                similar = onto_access.getClassIRIsContainingName(t2)
                labels = onto_access.getDescendantNames(similar)
                label = random.sample(labels, k=1)
                labels.append(label[0])
                # print(label[0])
            except:
                pass
    # print('\n types', types)
    # print('labels', labels)
    return labels


df['sibling_type'] = df['type'].apply(get_sibling)   # column by column


# shuffle the answer categories and types independent of the questions to get a random answer category/type

df['output_column'] = df['type'].copy()
n_rows = len(df['type'])
pick_new_rows = np.random.permutation(list(range(n_rows)))[0:n_rows]
shuffled_values = np.random.permutation(df['output_column'][pick_new_rows])
df['output_column'][pick_new_rows] = shuffled_values
print('done shuffle')

df_csv_test = df[0:20]
print(df_csv_test.shape)

df_csv_test.to_csv('data/df2.csv')
print('done read to csv')

# separate positive and negative samples

df_positive = pd.read_csv('data/df.csv')
df_negative = df[["category",
                  "type",
                  "question",
                  "wh",
                  "id",
                  "sibling_type",
                  "output_column"
                  ]]    # subset of df
'''
category	
concatenated_vector	
entities	
entities_KGE_vector	
entity_types	
found category	
found type	
id	
noun list	
np list	
question	
type	
we_nouns_vector	
we_np_vector	
we_type_vector	
we_wh_vector	
wh	
sibling_type	
output_column
'''

# check sample is actually negative
df_negative2 = df_negative[(df_negative.output_column != df_negative.type)]

# pickle
f = open('data/positive_samples.pkl', 'wb')
pickle.dump(df_positive, f)
f.close()

f = open('data/negative_samples.pkl', 'wb')
pickle.dump(df_negative2, f)
f.close()

print('done pickled')
