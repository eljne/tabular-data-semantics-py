'''train a MLP model for each category and type'''

import pickle
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier

# use only original training data
pkl_file = open('data/positive_samples.pkl', 'rb')
load = pickle.load(pkl_file)
pkl_file.close()

positive_samples = pd.DataFrame(load)

'''split on types/categories again'''


def unique_array_workaround(series):
    series2 = []
    for item in series:
        item2 = str(item)
        if item2 != '[]' and item2 != []:   # get rid of label = []
            series2.append(item2)
    typez = list(set(series2))
    return typez


categories = positive_samples['category'].unique()
types = unique_array_workaround(positive_samples['type'])

positive_samples['type tuple'] = positive_samples['type'].map(tuple)
types_dfs = [pd.DataFrame(y) for x, y in positive_samples.groupby('type tuple', as_index=False)]
cats_dfs = [pd.DataFrame(y) for x, y in positive_samples.groupby('category', as_index=False)]

print('done split to types and categories')


def random_sample_ratioed(datafrm, pos_fraction, ratio_pos, ratio_neg):
    # fraction is a ratio e.g.
    positive = datafrm[datafrm['y'] == 1]
    negative = datafrm[datafrm['y'] == 0]
    positive_smples = positive.sample(frac=pos_fraction, random_state=0)
    neg_samples_wanted = ((len(positive_smples) / ratio_pos) * ratio_neg)  # make sure this is correct! do some math!
    fraction2 = neg_samples_wanted / len(negative)
    # print('pos', len(positive))
    # print('neg', len(negative))
    # print('pos sampled', len(positive_smples))
    # print('neg wanted', neg_samples_wanted)
    try:
        negative_smples = negative.sample(frac=fraction2, random_state=0)
        # print('neg sampled', len(negative_smples))
    except:
        print('not enough negative data, try diff ratio/fraction')
        return pd.DataFrame()
    new_df = pd.concat([positive_smples, negative_smples])  # append all data together
    new_df2 = new_df.sample(frac=1)  # shuffle dataframe
    return new_df2


def train_classifier(train, label):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 2), random_state=1)
    # print('label', label.shape)   # array y of size (n_samples,)
    # 8814    0
    # 11152   0
    # 3949    [[0.0223, 0.0816, 0.0139, -0.0124, -0.0084, -0...
    # print('train', train.shape)   # array X of size (n_samples, n_features)
    clf.fit(list(train), label)   # debug from here
    return clf


'''select positive samples at random from training data'''
classifiers_pos_typ = dict.fromkeys(types)
classifiers_pos_cat = dict.fromkeys(categories)
print('classifiers_pos_cat', classifiers_pos_cat)
print('classifiers_pos_typ', classifiers_pos_typ)


def label_polarity(row, label, column):
    if row[column] == label or str(row[column]) == label:  # if category is current label
        return 1  # positive polarity
    else:
        return 0  # negative polarity


for df in cats_dfs:
    copy_ds = positive_samples.copy()
    cat_label = df["category"].unique()
    copy_ds["y"] = copy_ds.apply(lambda row: label_polarity(row, cat_label, 'category'), axis=1)
    train_set = random_sample_ratioed(copy_ds, 0.80, 1, 1)  # split differently according to pos/neg balance
    # print(train_set)
    # X = train_set['concatenated_vector']
    X = train_set['we_np_vector']
    y = train_set["y"]
    classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
    classifiers_pos_cat[cat_label[0]] = classifier


for df in types_dfs:
    copy_ds2 = positive_samples.copy()
    typ_label = unique_array_workaround(df["type"])
    print('label', typ_label)
    copy_ds2["y"] = copy_ds2.apply(lambda row: label_polarity(row, typ_label, 'type'), axis=1)  # get rows that match
    # the type
    train_set = random_sample_ratioed(copy_ds2, 0.80, 1, 1)  # split differently according to pos/neg balance
    # print(train_set)
    # X = train_set['concatenated_vector']
    X = train_set['we_np_vector']
    y = train_set["y"]
    classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
    classifiers_pos_typ[typ_label] = classifier

# for df in types_dfs:
#     type_label = unique_array_workaround(df["type"])
#     print(type_label)

# classifier = train_classifier(train_set['concatenated_vector'], type_label)
# classifiers_pos_typ[type_label] = classifier


# f = open('data/classifiers_pos_cat.pkl', 'rb')
# pickle.dump(classifiers_pos_cat, f)
# pkl_file.close()


#
# f = open('data/classifiers_pos_typ.pkl', 'rb')
# pickle.dump(classifiers_pos_typ,f)
# pkl_file.close()
#
