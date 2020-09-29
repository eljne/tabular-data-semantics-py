''' reformat concatenated vectors so they work with classifiers '''
'''Eleanor Bill'''
from kg.EB_classes import unpickle, pickl
import pandas as pd

all_td = unpickle('training_vectors/31_all_td_fin')
all_td = pd.DataFrame(all_td)


def reformat(row_column):
    concatenated_vector_2 = []
    for component in row_column:
        component_list = component.tolist()
        concatenated_vector_2.append(component_list)
    print('..')
    return concatenated_vector_2


all_td['concatenated_vector_2'] = all_td['concatenated_vector'].apply(reformat)
all_td2 = all_td.drop(['concatenated_vector',
                       'we_nouns_vector',
                       'we_type_vector',
                       'we_wh_vector',
                       'wh',
                       'entities_KGE_vector'], axis=1)
all_td3 = all_td2.rename(columns={'concatenated_vector_2': 'concatenated_vector'})
pickl('training_vectors/32_all_td_justconcat', all_td3)
