''' author: Eleanor Bill @eljne '''
''' join all data - lots of renaming and dropping fields'''

from kg.EB_classes import pickl, unpickle
import numpy as np
import pandas as pd

# unpickle all vectors
negative_all = unpickle('df_negative_fin')
new_positive = unpickle('df_positive_fin2')
og_positive = unpickle('df')
print('unpickled')
# rejig - renaming etc. to get consistency

''' NEGATIVE '''
negative_all2 = negative_all.drop(['new we_type_vector', 'type'], axis=1)
negative_all3 = negative_all2.rename(columns={'new avg we_type_vector': 'we_type_vector'})
negative_shuffle = negative_all3
negative_sibling = negative_all3
negative_shuffle2 = negative_shuffle.drop(['category'], axis=1)
negative_shuffle3 = negative_shuffle2.rename(columns={'shuffled_category': 'category',
                                                      'shuffled_type': 'type'})
negative_shuffle4 = negative_shuffle3.drop(['sibling_type'], axis=1)
negative_sibling2 = negative_sibling.rename(columns={'sibling_type': 'type'})
negative_sibling3 = negative_sibling2.drop(['shuffled_category', 'shuffled_type'], axis=1)
print(list(negative_shuffle4.columns.values))
print(list(negative_sibling3.columns.values))
negative_all4 = negative_sibling2.append(negative_shuffle3)

'''
['category', 'concatenated_vector', 'entities_KGE_vector', 'id', 'we_type_vector', 'polarity', 'question', 'type', 
'we_nouns_vector', 'we_wh_vector', 'wh']'''

'''ORIGINAL POSITIVE'''

og_positive['polarity'] = "1"
og_positive2 = og_positive.drop(['found category', 'found type', 'noun list', 'np list', 'entities', 'entity_types'
                                                                                                     ''],
                                axis=1)
print(list(og_positive2.columns.values))

'''
['category', 'concatenated_vector', 'entities_KGE_vector', 'id', 'we_type_vector', 'polarity', 'question', 'type',
'we_nouns_vector', 'we_wh_vector', 'wh']'''

''' NEW POSITIVE '''

new_positive2 = new_positive.drop(['noun list',
                                   'np list',
                                   'additional noun list',
                                   'additional np list',
                                   'new nps2',
                                   'new nouns',
                                   'new we_nouns_vector',
                                   'new entities_KGE_vector',
                                   'new we_type_vector',
                                   'entity',
                                   'new entity types'
                                   ], axis=1)

new_positive3 = new_positive2.rename(columns={'new_concatenated_vector': 'concatenated_vector',
                                              'new avg we_nouns_vector': 'we_nouns_vector',
                                              'new avg entities_KGE_vector': 'entities_KGE_vector',
                                              'new avg we_type_vector': 'we_type_vector'
                                              })

print(list(new_positive3.columns.values))

'''
['category', 'concatenated_vector', 'entities_KGE_vector', 'id', 'we_type_vector', 'polarity', 'question', 'type',
'we_wh_vector', 'we_nouns_vector', 'wh']
'''

# append together
new_td = negative_all4.append(og_positive2)
all_td = new_td.append(new_positive3)

# pickle all training data
pickl('all_td', all_td)
print('pickled')
