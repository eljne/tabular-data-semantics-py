from kg.EB_classes import unpickle
import pandas as pd

# df = unpickle('dbpedia_test_final')
# df2 = pd.DataFrame(df)
# df3 = df2[0:100]
# df3.to_csv('data/test code/test_vectors.csv')

# classifiers_pos_cat = unpickle('classifiers_pos_cat')
# print(classifiers_pos_cat)
#
# classifiers_pos_typ = unpickle('classifiers_pos_typ')
# print(classifiers_pos_typ)

# test_data = unpickle('test_data')
# test_data = test_data[0:100]
# test_data.to_csv('data/test_data.csv')
# print(test_data.type_scores)

'''vector tests'''

# checking shape of concatenated vectors
og_positive = unpickle('training_vectors/final_original_training_vectors')
for a in og_positive['concatenated_vector']:
    print(len(a[0]))
    print(len(a[1]))
    print(len(a[2]))
    print(len(a[3]))
    print(len(a[4]))
og_positive = og_positive[0:20]
og_positive.to_csv('data/test code/og_positive.csv')

# test vectors
test_vectors = unpickle('testing_vectors/10_dbpedia_test_fin')
test_vectors = pd.DataFrame(test_vectors)
for a in test_vectors['we_nouns_vector']:
    print(len(a))
for a in test_vectors['concatenated_vector']:
    print(len(a))
    print(len(a[0]))
    print(len(a[1]))
    print(len(a[2]))
    print(len(a[3]))
    print(len(a[4]))
test_vectors = test_vectors[0:20]
test_vectors.to_csv('data/test code/tests.csv')

# all training data
all_td = unpickle('training_vectors/31_all_td_fin')
test_vectors = pd.DataFrame(test_vectors)
for a in test_vectors['we_nouns_vector']:
    print(len(a))
for a in test_vectors['concatenated_vector']:
    print(len(a))
    print(len(a[0]))
    print(len(a[1]))
    print(len(a[2]))
    print(len(a[3]))
    print(len(a[4]))
all_td = all_td[0:20]
all_td.to_csv('data/test code/all_td.csv')
