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

# checking shape of concatenated vectors
# og_positive = unpickle('df')
# for a in og_positive['concatenated_vector']:
    # print(len(a[0]))
    # print(len(a[1]))
    # print(len(a[2]))
    # print(len(a[3]))
    # print(len(a[4]))

# # all td
all_td = unpickle('all_td2')
for a in all_td['entities_KGE_vector']:
    print(len(a))

for a in all_td['concatenated_vector']:
    print(len(a))
    print(len(a[0]))
    print(len(a[1]))
    print(len(a[2]))
    print(len(a[3]))
    print(len(a[4]))


# test vectors
# tests = unpickle('dbpedia_test_final')
# tests = pd.DataFrame(tests)
# for a in tests['we_nouns_vector']:
#     print(len(a))
# for a in tests['concatenated_vector']:
#     print(len(a))
#     print(len(a[0]))
#     print(len(a[1]))
#     print(len(a[2]))
#     print(len(a[3]))
#     print(len(a[4]))