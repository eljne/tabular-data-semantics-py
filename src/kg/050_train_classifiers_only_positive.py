'''train a MLP model for each category and type'''

import pickle
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier

pkl_file = open('data/positive_samples.pkl', 'rb')
positive_samples = pickle.load(pkl_file)
pkl_file.close()

'''split on types/categories again'''

types = positive_samples['type'].unique()
categories = positive_samples['category'].unique()

types_dfs = [pd.DataFrame(y) for x, y in positive_samples.groupby('type', as_index=False)]
cats_dfs = [pd.DataFrame(y) for x, y in positive_samples.groupby('category', as_index=False)]

print('done split to types and categories')


def train_test(dataset, fraction):
    train_set = dataset.sample(frac=fraction, random_state=0)
    test_set = dataset.drop(train_set.index)
    return train_set, test_set


def train_classifier(train_set, label):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(train_set, label)
    return clf


'''select positive samples at random from training data'''
classifiers_pos_cat = {}
classifiers_pos_typ = {}

# for df in types_dfs:
    # train_set, test_set = train_test(df, 0.80)
    # type_label = df["type"].unique()
    # print(type_label)
    # classifier = train_classifier(train_set['concatenated_vector'], type_label)
    # classifiers_pos_typ[type_label] = classifier

for df in cats_dfs:
    train_set, test_set = train_test(df, 0.80)
    cat_label = df["category"].unique()
    training_vector = pd.Series()
    for a in train_set['concatenated_vector']:
        print(a)
        b = a.tolist()
        training_vector.append(b)
    classifier = train_classifier(training_vector, cats_dfs) # need to convert vector from list of arrays to matrix
    classifiers_pos_cat[cats_dfs] = classifier


f = open('data/classifiers_pos_cat.pkl', 'rb')
pickle.dump(classifiers_pos_cat, f)
pkl_file.close()
#
# f = open('data/classifiers_pos_typ.pkl', 'rb')
# pickle.dump(classifiers_pos_typ,f)
# pkl_file.close()
#
