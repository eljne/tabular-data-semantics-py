''' author: Eleanor Bill @eljne '''
''' join all data '''
from kg.EB_classes import pickl, unpickle

# unpickle all vectors
negative_all = unpickle('df_negative_fin')
new_positive = unpickle('df_positive_fin')
og_positive = unpickle('df')

# rejig - renaming etc. to get consistency

'''
NEGATIVE:

category
concatenated_vector
entities_KGE_vector
id
new avg we_type_vector
new we_type_vector
polarity
question
shuffled_category
shuffled_type
sibling_type
type
we_nouns_vector
we_np_vector
we_wh_vector
wh
'''

negative_all2 = negative_all.drop(['new we_type_vector'], axis=0)

negative_all3 = negative_all2.rename(columns={'new avg we_type_vector': 'we_type_vector'
                                              }
                                     , inplace=True)

'''
POSITIVE:

'''

new_positive2 = new_positive.drop(['concatenated_vector',
                                   'we_nouns_vector',
                                   'we_np_vector',
                                   'entities_KGE_vector',
                                   'we_type_vector',
                                   'new we_nouns_vector',
                                   'new we_np_vector',
                                   'new entities_KGE_vector',
                                   'new we_type_vector'
                                   ], axis=0)

new_positive3 = new_positive2.rename(columns={'new_concatenated_vector': 'concatenated_vector',
                                              'new avg we_nouns_vector': 'we_nouns_vector',
                                              'new avg we_np_vector': 'we_np_vector',
                                              'new avg entities_KGE_vector': 'entities_KGE_vector',
                                              'new avg we_type_vector': 'we_type_vector'
                                              }
                                     , inplace=True)

# append together
new_td = negative_all.append(new_positive3)
all_td = new_td.append(og_positive)

# pickle all training data
pickl('all_td', all_td)
