from kg.EB_classes import unpickle
import pandas as pd

'''vector tests'''

# checking shape of concatenated vectors
og_positive = unpickle('training_vectors/final_original_training_vectors')
for a in og_positive['concatenated_vector']:
    print(len(a))
    print(len(a[0]))
    print(len(a[1]))
    print(len(a[2]))
    print(len(a[3]))
og_positive = og_positive[0:20]
og_positive.to_csv('data/test code/og_positive.csv')

# test vectors
test_vectors = unpickle('testing_vectors/10_dbpedia_test_fin')
test_vectors = pd.DataFrame(test_vectors)
for a in test_vectors['concatenated_vector']:
    print(len(a))
    print(len(a[0]))
    print(len(a[1]))
    print(len(a[2]))
    print(len(a[3]))
test_vectors = test_vectors[0:20]
test_vectors.to_csv('data/test code/tests.csv')

# all training data
all_td = unpickle('training_vectors/31_all_td_fin')
test_vectors = pd.DataFrame(test_vectors)
for a in test_vectors['concatenated_vector']:
    print(len(a))
    print(len(a[0]))
    print(len(a[1]))
    print(len(a[2]))
    print(len(a[3]))
all_td = all_td[0:20]
all_td.to_csv('data/test code/all_td.csv')

