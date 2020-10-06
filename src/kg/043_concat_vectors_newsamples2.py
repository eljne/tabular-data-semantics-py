''' author: Eleanor Bill @eljne '''
''' join all data - lots of renaming and dropping fields'''

from kg.EB_classes import pickl, unpickle
import numpy as np
import pandas as pd

all_td = unpickle('training_vectors/30_all_td')
all_td = pd.DataFrame(all_td).reset_index()
all_td = all_td.fillna(0)
all_td['entities_KGE_vector_2'] = all_td['we_wh_vector'].copy()

pd.set_option('mode.chained_assignment', None)
# make sure all the same length (if returned zeros, replace with array of zeroes that is correct length)
for a in range(0, len(all_td)):
    try:
        if len(all_td['we_wh_vector'][a]) == 1:
            all_td['we_wh_vector'][a] = np.zeros(300)
    except:
        try:
            if all_td['we_wh_vector'][a] == 0:
                all_td['we_wh_vector'][a] = np.zeros(300)
        except:
            print('1', all_td['we_wh_vector'][a])

    try:
        if len(all_td['we_nouns_vector'][a]) == 1:
            all_td['we_nouns_vector'][a] = np.zeros(300)
    except:
        try:
            if all_td['we_nouns_vector'][a] == 0:
                all_td['we_nouns_vector'][a] = np.zeros(300)
        except:
            print('2', all_td['we_nouns_vector'][a])

    try:
        if len(all_td['entities_KGE_vector'][a]) == 200:
            all_td['entities_KGE_vector_2'][a] = all_td['entities_KGE_vector'][a]
        else:
            all_td['entities_KGE_vector_2'][a] = np.zeros(200)
    except:
        try:
            if all_td['entities_KGE_vector'][a] == 0:
                all_td['entities_KGE_vector_2'][a] = np.zeros(200)
        except:
            all_td['entities_KGE_vector_2'][a] = np.zeros(200)  # returning float 0.0

    try:
        if len(all_td['we_type_vector'][a]) == 1:
            all_td['we_type_vector'][a] = np.zeros(300)
    except:
        try:
            if all_td['we_type_vector'][a] == 0:
                all_td['we_type_vector'][a] = np.zeros(300)
        except:
            print('4', all_td['we_type_vector'][a])

    # print('we_wh_vector', len(dbpedia_train_wh['we_wh_vector'][a]))   # 300
    # print('we_nouns_vector', len(dbpedia_train_wh['we_nouns_vector'][a]))  # 300
    # print('entities_KGE_vector', len(dbpedia_train_wh['entities_KGE_vector_2'][a]))  # 200
    # print('we_type_vector', len(dbpedia_train_wh['we_type_vector'][a]))  # 300
    print(('...'))

# rebuild concatenated vectors
all_td2 = all_td.drop(['concatenated_vector', 'entities_KGE_vector'], axis=1)
all_td3 = all_td2.rename(columns={'entities_KGE_vector_2': 'entities_KGE_vector'})
all_td3['con_wh_nouns'] = all_td3.apply(lambda x: [x['we_wh_vector'],
                                                   x['we_nouns_vector']], axis=1)
all_td3['con_wh_kge'] = all_td3.apply(lambda x: [x['we_wh_vector'],
                                                 x['entities_KGE_vector']], axis=1)
all_td3['con_nouns_KGE'] = all_td3.apply(lambda x: [x['we_nouns_vector'],
                                                    x['entities_KGE_vector']], axis=1)
all_td3['con_wh_nouns_kge'] = all_td3.apply(lambda x: [x['we_wh_vector'],
                                                       x['we_nouns_vector'],
                                                       x['entities_KGE_vector']], axis=1)
all_td3['con_wh_kge_types'] = all_td3.apply(lambda x: [x['we_wh_vector'],
                                                       x['entities_KGE_vector'],
                                                       x['we_type_vector']], axis=1)
all_td3['concatenated_vector'] = all_td3.apply(lambda x: [x['we_wh_vector'],
                                                          x['we_nouns_vector'],
                                                          x['entities_KGE_vector'],
                                                          x['we_type_vector']], axis=1)
pickl('training_vectors/31_all_td_fin', all_td3)
print('pickled')
