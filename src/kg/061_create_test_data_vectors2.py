''' author: Eleanor Bill @eljne '''
''' create vectors for test data '''
import numpy as np
import pandas as pd
from kg.EB_classes import pickl, unpickle

dbpedia_test = unpickle('testing_vectors/09_dbpedia_test')

# check for arrays length 1

dbpedia_test = pd.DataFrame(dbpedia_test)
dbpedia_test = dbpedia_test.fillna(0)
dbpedia_test['entities_KGE_vector_2'] = dbpedia_test['we_wh_vector'].copy()

pd.set_option('mode.chained_assignment', None)
# make sure all the same length (if returned zeros, replace with array of zeroes that is correct length)
for a in range(0, len(dbpedia_test)):
    try:
        if len(dbpedia_test['we_wh_vector'][a]) == 1:
            dbpedia_test['we_wh_vector'][a] = np.zeros(300)
    except:
        try:
            if dbpedia_test['we_wh_vector'][a] == 0:
                dbpedia_test['we_wh_vector'][a] = np.zeros(300)
        except:
            print('1', dbpedia_test['we_wh_vector'][a])

    try:
        if len(dbpedia_test['we_nouns_vector'][a]) == 1:
            dbpedia_test['we_nouns_vector'][a] = np.zeros(300)
    except:
        try:
            if dbpedia_test['we_nouns_vector'][a] == 0:
                dbpedia_test['we_nouns_vector'][a] = np.zeros(300)
        except:
            print('2', dbpedia_test['we_nouns_vector'][a])

    try:
        if len(dbpedia_test['entities_KGE_vector'][a]) == 200:
            dbpedia_test['entities_KGE_vector_2'][a] = dbpedia_test['entities_KGE_vector'][a]
        else:
            dbpedia_test['entities_KGE_vector_2'][a] = np.zeros(200)
    except:
        try:
            if dbpedia_test['entities_KGE_vector'][a] == 0:
                dbpedia_test['entities_KGE_vector_2'][a] = np.zeros(200)
        except:
            dbpedia_test['entities_KGE_vector_2'][a] = np.zeros(200)  # returning float 0.0

    try:
        if len(dbpedia_test['we_type_vector'][a]) == 1:
            dbpedia_test['we_type_vector'][a] = np.zeros(300)
    except:
        try:
            if dbpedia_test['we_type_vector'][a] == 0:
                dbpedia_test['we_type_vector'][a] = np.zeros(300)
        except:
            print('4', dbpedia_test['we_type_vector'][a])


def concatenate_vector(entry):
    cv = [entry['we_wh_vector'],
          entry['we_nouns_vector'],
          entry['entities_KGE_vector_2'],
          entry['we_type_vector']]
    return cv


dbpedia_test['concatenated_vector'] = dbpedia_test.apply(concatenate_vector, axis=1)
dbpedia_test2 = dbpedia_test.drop(['entities_KGE_vector'], axis=1)
dbpedia_test3 = dbpedia_test2.rename(columns={'entities_KGE_vector_2': 'entities_KGE_vector'})
dbpedia_test3['con_wh_nouns'] = dbpedia_test3.apply(lambda x: [x['we_wh_vector'],
                                                               x['we_nouns_vector']], axis=1)
dbpedia_test3['con_wh_kge'] = dbpedia_test3.apply(lambda x: [x['we_wh_vector'],
                                                             x['entities_KGE_vector']], axis=1)
dbpedia_test3['con_nouns_KGE'] = dbpedia_test3.apply(lambda x: [x['we_nouns_vector'],
                                                                x['entities_KGE_vector']], axis=1)
dbpedia_test3['con_wh_nouns_kge'] = dbpedia_test3.apply(lambda x: [x['we_wh_vector'],
                                                                   x['we_nouns_vector'],
                                                                   x['entities_KGE_vector']], axis=1)
dbpedia_test3['con_wh_kge_types'] = dbpedia_test3.apply(lambda x: [x['we_wh_vector'],
                                                                   x['entities_KGE_vector'],
                                                                   x['we_type_vector']], axis=1)
dbpedia_test3['concatenated_vector'] = dbpedia_test3.apply(lambda x: [x['we_wh_vector'],
                                                                      x['we_nouns_vector'],
                                                                      x['entities_KGE_vector'],
                                                                      x['we_type_vector']], axis=1)
pickl('testing_vectors/10_dbpedia_test_fin', dbpedia_test3)
