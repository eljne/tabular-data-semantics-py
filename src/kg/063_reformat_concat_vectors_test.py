''' reformat concatenated vectors so they work with classifiers '''
'''Eleanor Bill'''
from kg.EB_classes import unpickle, pickl
import pandas as pd

dbpedia_test = unpickle('testing_vectors/10_dbpedia_test_fin')
dbpedia_test = pd.DataFrame(dbpedia_test)


def reformat(row_column):
    concatenated_vector_2 = []
    for component in row_column:
        component_list = component.tolist()
        concatenated_vector_2.append(component_list)
    print('..')
    return concatenated_vector_2


dbpedia_test['concatenated_vector_2'] = dbpedia_test['concatenated_vector'].apply(reformat)
dbpedia_test2 = dbpedia_test.drop(['concatenated_vector'], axis=1)
dbpedia_test3 = dbpedia_test2.rename(columns={'concatenated_vector_2': 'concatenated_vector'})
pickl('testing_vectors/11_dbpedia_test_fin', dbpedia_test3)
