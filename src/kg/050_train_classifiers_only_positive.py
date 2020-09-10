'''train a MLP model for each category and type'''

import pickle
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier

pkl_file = open('data/positive_samples.pkl', 'rb')
load = pickle.load(pkl_file)
pkl_file.close()

positive_samples = pd.DataFrame(load)

'''split on types/categories again'''


def unique_array_workaround(series):
    series2 = []
    for item in series:
        item2 = str(item)
        series2.append(item2)
    typez = list(set(series2))
    return typez


categories = positive_samples['category'].unique()
types = unique_array_workaround(positive_samples['type'])


positive_samples['type tuple'] = positive_samples['type'].map(tuple)
types_dfs = [pd.DataFrame(y) for x, y in positive_samples.groupby('type tuple', as_index=False)]
cats_dfs = [pd.DataFrame(y) for x, y in positive_samples.groupby('category', as_index=False)]

print('done split to types and categories')


def train_test(datafrm, fraction):
    train = datafrm.sample(frac=fraction, random_state=0)
    test = datafrm.drop(train.index)
    return train, test


def train_classifier(train, label):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 2), random_state=1)
    print('label', label)
    print('train', train)
    clf.fit(train, label)
    return clf


'''select positive samples at random from training data'''
classifiers_pos_cat = {}
classifiers_pos_typ = {}

for df in cats_dfs:
    copy_ds = positive_samples.copy()
    cat_label = df["category"].unique()  # convert label to array y of size (n_samples,)
    if copy_ds["category"] == cat_label:  # if category is current label
        copy_ds["y"] = 1    # positive polarity
    else:
        copy_ds["y"] = 0    # negative polarity
    train_set, test_set = train_test(copy_ds, 0.80) # split differently according to pos/neg balance

    print(len(df["category"]))
    X = train_set['concatenated_vector'] # array X of size (n_samples, n_features)
    classifier = train_classifier(X, y)   # need to convert vector from list of
    # arrays to matrix
    classifiers_pos_cat[cats_dfs] = classifier


# for df in types_dfs:
    # train_set, test_set = train_test(df, 0.80)
    # type_label = unique_array_workaround(df["type"])
    # print(type_label)
    # classifier = train_classifier(train_set['concatenated_vector'], type_label)
    # classifiers_pos_typ[type_label] = classifier


f = open('data/classifiers_pos_cat.pkl', 'rb')
pickle.dump(classifiers_pos_cat, f)
pkl_file.close()
#
# f = open('data/classifiers_pos_typ.pkl', 'rb')
# pickle.dump(classifiers_pos_typ,f)
# pkl_file.close()
#
