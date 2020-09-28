''' author: Eleanor Bill @eljne '''
''' concatenate vectors and export to dataframe/csv '''

import pandas as pd
import numpy as np
from kg.EB_classes import unpickle, pickl
dbpedia_train_wh = unpickle('dbpedia_train_all_vectors')


'''
we_wh_vector - First position could be for the embedding of the wh question word (we can create our own embedding/encoding).
we_nouns_vector - Second position for the WE of the sentence or set of nouns.
we_np_vector - Third position (up to 3 or 4 vector positions? we can play with different values) for noun phrases without a good correspondence in KG (WE of the noun phrase)
entities_KGE_vector - Fourth position (up to 3 or 4 vector positions) for noun phrases with a good correspondence in KG (KGE of entity representing noun phrase)
we_type_vector - Fifth position (up to 3 or 4 vector positions) for the WE of the types of the KG entities above.
'''

dbpedia_train_wh = pd.DataFrame(dbpedia_train_wh)
dbpedia_train_wh = dbpedia_train_wh.fillna(0)
dbpedia_train_wh['entities_KGE_vector_2'] = dbpedia_train_wh['we_wh_vector'].copy()

pd.set_option('mode.chained_assignment', None)
# make sure all the same length (if returned zeros, replace with array of zeroes that is correct length)
for a in range(0, len(dbpedia_train_wh)):
    try:
        if len(dbpedia_train_wh['we_wh_vector'][a]) == 1:
            dbpedia_train_wh['we_wh_vector'][a] = np.zeros(300)
    except:
        try:
            if dbpedia_train_wh['we_wh_vector'][a] == 0:
                dbpedia_train_wh['we_wh_vector'][a] = np.zeros(300)
        except:
            print('1', dbpedia_train_wh['we_wh_vector'][a])

    try:
        if len(dbpedia_train_wh['we_nouns_vector'][a]) == 1:
            dbpedia_train_wh['we_nouns_vector'][a] = np.zeros(300)
    except:
        try:
            if dbpedia_train_wh['we_nouns_vector'][a] == 0:
                dbpedia_train_wh['we_nouns_vector'][a] = np.zeros(300)
        except:
            print('2', dbpedia_train_wh['we_nouns_vector'][a])

    try:
        if len(dbpedia_train_wh['we_np_vector'][a]) == 1:
            dbpedia_train_wh['we_np_vector'][a] = np.zeros(300)
    except:
        try:
            if dbpedia_train_wh['we_np_vector'][a] == 0:
                dbpedia_train_wh['we_np_vector'][a] = np.zeros(300)
        except:
            print('3', dbpedia_train_wh['we_np_vector'][a])

    try:
        if len(dbpedia_train_wh['entities_KGE_vector'][a]) == 200:
            dbpedia_train_wh['entities_KGE_vector_2'][a] = dbpedia_train_wh['entities_KGE_vector'][a]
        else:
            dbpedia_train_wh['entities_KGE_vector_2'][a] = np.zeros(200)
    except:
        try:
            if dbpedia_train_wh['entities_KGE_vector'][a] == 0:
                dbpedia_train_wh['entities_KGE_vector_2'][a] = np.zeros(200)
        except:
            dbpedia_train_wh['entities_KGE_vector_2'][a] = np.zeros(200)  # returning float 0.0

    try:
        if len(dbpedia_train_wh['we_type_vector'][a]) == 1:
            dbpedia_train_wh['we_type_vector'][a] = np.zeros(300)
    except:
        try:
            if dbpedia_train_wh['we_type_vector'][a] == 0:
                dbpedia_train_wh['we_type_vector'][a] = np.zeros(300)
        except:
            print('5', dbpedia_train_wh['we_type_vector'][a])

    # print('we_wh_vector', len(dbpedia_train_wh['we_wh_vector'][a]))   # 300
    # print('we_nouns_vector', len(dbpedia_train_wh['we_nouns_vector'][a]))  # 300
    # print('we_np_vector', len(dbpedia_train_wh['we_np_vector'][a]))   # 300
    # print('entities_KGE_vector', len(dbpedia_train_wh['entities_KGE_vector_2'][a]))  # 200
    # print('we_type_vector', len(dbpedia_train_wh['we_type_vector'][a]))  # 300

dbpedia_train_wh['concatenated_vector'] = dbpedia_train_wh.apply(lambda x: [x['we_wh_vector'],
                                                                            x['we_nouns_vector'],
                                                                            x['we_np_vector'],
                                                                            x['entities_KGE_vector_2'],
                                                                            x['we_type_vector']], axis=1)


dbpedia_train_wh2 = dbpedia_train_wh.drop(['entities_KGE_vector'], axis=1)
dbpedia_train_wh3 = dbpedia_train_wh2.rename(columns={'entities_KGE_vector_2': 'entities_KGE_vector'})

print('done concatenate vector')

df_sample = dbpedia_train_wh3[0:10]
df_sample.to_csv('data/df_sample.csv')
print('done sampled to csv')

pickl('df', dbpedia_train_wh3)
print('done pickled')