'''author: Eleanor Bill @eljne'''
''' queries training data '''
from kg.EB_classes import load_json
import numpy as np
import pandas as pd
from kg.EB_classes import unpickle

# dbpedia_train = load_json("data/smarttask_dbpedia_train")
# df = pd.DataFrame(dbpedia_train)
#
#
# def flat(val):
#     v = np.asarray(val)
#     v2 = v.flatten()
#     return str(v2)
#
#
# df['flat list'] = df['type'].apply(flat)
# df['test'] = df['flat list'].str.contains('Location')
# df2 = df[df['test'] == True]
# print(df2)
# df2.to_csv('data/query.csv')


'''output to csvs and test components of vectors'''

# checking shape of concatenated vectors
# og_positive = unpickle('training_vectors/final_original_training_vectors')
# for a in og_positive['concatenated_vector']:
#     print(len(a))
#     print(len(a[0]))
#     print(len(a[1]))
#     print(len(a[2]))
#     print(len(a[3]))
# og_positive = og_positive[0:20]
# og_positive.to_csv('data/test code/og_positive.csv')

# test vectors
# test_vectors = unpickle('testing_vectors/10_dbpedia_test_fin')
# test_vectors = pd.DataFrame(test_vectors)
# for a in test_vectors['concatenated_vector']:
#     print(len(a))
#     print(len(a[0]))
#     print(len(a[1]))
#     print(len(a[2]))
#     print(len(a[3]))
# test_vectors = test_vectors[0:20]
# test_vectors.to_csv('data/test code/tests.csv')

# all training data
# all_td = unpickle('training_vectors/31_all_td_fin')
# all_td = pd.DataFrame(all_td)
# for a in all_td['concatenated_vector']:
#     print(len(a))
#     print(len(a[0]))
#     print(len(a[1]))
#     print(len(a[2]))
#     print(len(a[3]))
# all_td = all_td[0:20]
# all_td.to_csv('data/test code/all_td.csv')

# test reformatting concatenated vectors
# all_td = unpickle('training_vectors/31_all_td_fin')
# all_td = pd.DataFrame(all_td)
# all_td = all_td[0:20]
#
#
# def reformat(row_column):
#     concatenated_vector_2 = []
#     for component in row_column:
#         component_list = component.tolist()
#         concatenated_vector_2.append(component_list)
#     return concatenated_vector_2
#
#
# all_td['concatenated_vector_2'] = all_td['concatenated_vector'].apply(reformat)
# all_td.to_csv('data/test code/reformat_concatvec.csv')

# check results formatting
results = unpickle('results/results_ALLTD')
results = results[0:10]
results.to_csv('data/test code/results.csv')

# testing_vectors = unpickle('testing_vectors/11_dbpedia_test_fin')
# testing_vectors = testing_vectors[0:10]
# testing_vectors.to_csv('data/test code/testing_vectors.csv')

# results = unpickle('training_vectors/final_original_training_vectors')
# results = results[0:10]
# results.to_csv('data/test code/final_original_training_vectors.csv')
#
# results = unpickle('training_vectors/final_original_training_vectors_minus_tests')
# results = results[0:10]
# results.to_csv('data/test code/final_original_training_vectors_minus_tests.csv')

# all training data
all_td = unpickle('test_data')
all_td = pd.DataFrame(all_td)
for a in all_td['con_wh_nouns']:
    print(len(a))
all_td = all_td[0:20]
all_td.to_csv('data/test code/all_td.csv')

# all_td = unpickle('train_data')
# all_td = pd.DataFrame(all_td)
# for a in all_td['con_wh_nouns']:
#     print(len(a))
# all_td = all_td[0:20]
# all_td.to_csv('data/test code/all_td.csv')


# all_td = unpickle('test_data')
# all_td = pd.DataFrame(all_td)
# for a in all_td['con_wh_nouns']:
#     print(len(a))
#     print(len(a[0]))
#     print(len(a[1]))
#     print(len(a[2]))
#     print(len(a[3]))
# all_td = all_td[0:20]
# all_td.to_csv('data/test code/all_td.csv')