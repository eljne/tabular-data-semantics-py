''' join all data '''
from kg.EB_classes import pickl, unpickle, nouns_list, noun_phrases_list, get_entities, apply_endpoint

# unpickle all vectors
negative_all = unpickle('df_negative_fin')
new_positive = unpickle('df_positive_fin')
og_positive = unpickle('df')

# rejig - renaming etc. to get consistency

# append together
# new_td = negative_all.append(new_positive)
# all_td = new_td.append(og_positive)

# pickle all training data
# pickl('all_td', all_td)


