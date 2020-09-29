''' author: Eleanor Bill @eljne '''
''' import csv, create negative samples from positive samples'''

import pandas as pd
import numpy as np
import random
from kg.EB_classes import unpickle, pickl
from ontology.onto_access import DBpediaOntology

# unpickle
load = unpickle('training_vectors/final_original_training_vectors')
df = pd.DataFrame(load)
print('done unpickled')

'''test different strategies to augment positive samples to get negative samples'''

# query for siblings of target types
# siblings of the classes associated with the target types e.g. ‘basketball player’ vs. ‘football player’
onto_access = DBpediaOntology()
onto_access.loadOntology(True)


def get_sibling(type):
    labels = []
    for t in type:
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

df['shuffled_type'] = df['type'].copy()
n_rows = len(df['type'])
pick_new_rows = np.random.permutation(list(range(n_rows)))[0:n_rows]
shuffled_values = np.random.permutation(df['shuffled_type'][pick_new_rows])
df['shuffled_type'][pick_new_rows] = shuffled_values
print('done type shuffle')

df['shuffled_category'] = df['category'].copy()
n_rows = len(df['category'])
pick_new_rows = np.random.permutation(list(range(n_rows)))[0:n_rows]
shuffled_values = np.random.permutation(df['shuffled_category'][pick_new_rows])
df['shuffled_category'][pick_new_rows] = shuffled_values
print('done category shuffle')

df_csv_test = df[0:20]
df_csv_test.to_csv('data/test code/negative_samples.csv')
print('done read extract to csv')

# separate positive and negative samples
df_negative = df[["category",
                  "type",
                  "question",
                  "wh",
                  "id",
                  "sibling_type",
                  "shuffled_type",
                  "shuffled_category",
                  "we_wh_vector",
                  "we_nouns_vector",
                  "entities_KGE_vector"
                  ]]    # subset of df

# labels for training samples: 0 for negative, 1 for positive
df_negative['polarity'] = "0"

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
we_type_vector	
we_wh_vector	
wh	
sibling_type	
shuffled_type
shuffled_category
'''

# check sample is actually negative
df_negative2 = df_negative[(df_negative.shuffled_type != df_negative.type)]
df_negative3 = df_negative2[(df_negative2.shuffled_category != df_negative2.category)]

pickl('training_vectors/21_train_new_negative_samples', df_negative3)
print('done pickled')
