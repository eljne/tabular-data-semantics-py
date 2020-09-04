'''train a MLP model for each category and type'''

import pickle
import numpy as np
from sklearn.neural_network import MLPClassifier

pkl_file = open('data/positive_samples.pkl', 'rb')
positive_samples = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('data/negative_samples.pkl', 'rb')
negative_samples = pickle.load(pkl_file)
pkl_file.close()

'''split on types/categories again'''

dict_of_types_pos = dict(iter(positive_samples.groupby('type')))
dict_of_categories_pos = dict(iter(positive_samples.groupby('category')))
dict_of_types_neg = dict(iter(negative_samples.groupby('type')))
dict_of_categories_neg = dict(iter(negative_samples.groupby('category')))

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

for category, df in dict_of_categories_neg:
    train_set, test_set = train_test(df, 0.80)
    classifier = train_classifier(train_set['concatenated_vector'], category)
    classifiers_pos_cat[category] = classifier


for type, df in dict_of_types_neg:
    train_set, test_set = train_test(df, 0.80)
    classifier = train_classifier(train_set['concatenated_vector'], type)
    classifiers_pos_typ[type] = classifier


f = open('data/classifiers_pos_cat.pkl', 'rb')
pickle.dump(classifiers_pos_cat,f)
pkl_file.close()

f = open('data/classifiers_pos_typ.pkl', 'rb')
pickle.dump(classifiers_pos_typ,f)
pkl_file.close()


'''use all training data'''
# append all training data
# how to train MLP using both positive and negative samples?


classifiers_all_cat = {}
classifiers_all_typ = {}

for category, df in dict_of_categories_all:
    train_set, test_set = train_test(df, 0.80)
    classifier = train_classifier(train_set['concatenated_vector'], category)
    classifiers_all_cat[category] = classifier

for type, df in dict_of_types_all:
    train_set, test_set = train_test(df, 0.80)
    classifier = train_classifier(train_set['concatenated_vector'], type)
    classifiers_all_typ[type] = classifier


f = open('data/classifiers_all_cat.pkl', 'rb')
pickle.dump(classifiers_all_cat,f)
pkl_file.close()

f = open('data/classifiers_all_typ.pkl', 'rb')
pickle.dump(classifiers_all_typ,f)
pkl_file.close()