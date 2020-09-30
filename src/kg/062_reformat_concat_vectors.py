''' reformat concatenated vectors so they work with classifiers '''
'''Eleanor Bill'''
from kg.EB_classes import unpickle, pickl
import pandas as pd
import pickle
import sys

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
all_td2 = all_td.drop(['concatenated_vector'], axis=1)
all_td3 = all_td2.rename(columns={'concatenated_vector_2': 'concatenated_vector'})


def save_as_pickled_object(obj, filepath):
    """
    This is a defensive way to write pickle.write, allowing for very large files on all platforms
    """
    max_bytes = 2**31 - 1
    bytes_out = pickle.dumps(obj)
    n_bytes = sys.getsizeof(bytes_out)
    with open(filepath, 'wb') as f_out:
        for idx in range(0, n_bytes, max_bytes):
            f_out.write(bytes_out[idx:idx+max_bytes])


save_as_pickled_object(all_td3, 'data/training_vectors/32_all_td_justconcat')

