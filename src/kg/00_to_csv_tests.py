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

test_data = unpickle('test_data')
test_data = test_data[0:100]
test_data.to_csv('data/test_data.csv')
# print(test_data.type_scores)
