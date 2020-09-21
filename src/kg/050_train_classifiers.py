''' author: Eleanor Bill @eljne '''
''' train a MLP model for each category and type '''

import pandas as pd
from kg.EB_classes import unpickle, get_last, pickl
from sklearn.neural_network import MLPClassifier

# use all training data
all_td = unpickle('all_td')
all_samples = pd.DataFrame(all_td)

'''split on types/categories again'''

categories = all_samples['category'].unique()
all_samples['fine type'] = all_samples['type'].apply(get_last)
types = all_samples['fine type'].unique()

types_dfs = [pd.DataFrame(y) for x, y in all_samples.groupby('fine type', as_index=False)] # just last one
cats_dfs = [pd.DataFrame(y) for x, y in all_samples.groupby('category', as_index=False)]

print('done split to types and categories')


def get_all(list):
    for t in list:
        types_all.append(t)
    return 0


# all types
types_all = []
all_samples['type'].apply(get_all)
types_all_unique = list(set(types_all))
print('all types', types_all_unique)


def random_sample_ratioed(datafrm, pos_fraction, ratio_pos, ratio_neg):
    # fraction is a ratio e.g.
    positive = datafrm[datafrm['y'] == 1]
    negative = datafrm[datafrm['y'] == 0]
    print('len pos', len(positive))
    print('len neg', len(negative))
    positive_smples = positive.sample(frac=pos_fraction, random_state=0)
    neg_samples_wanted = ((len(positive_smples) / ratio_pos) * ratio_neg)  # make sure this is correct! do some math!
    fraction2 = neg_samples_wanted / len(negative)
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
    # print('train', train.shape)   # array X of size (n_samples, n_features)
    clf.fit(list(train), label)   # debug from here
    return clf


dict_of_types = dict(iter(all_td.groupby('type')))
dict_of_categories = dict(iter(all_td.groupby('category')))


# choose the number of negative examples trained for each positive example

def label_polarity(row, label, column):
    if row[column] == label or str(row[column]) == label: # if type/category is current label
        if row['polarity'] == 1:    # and not already a negative sample
            return 1  # positive polarity
        else:   # if already a negative sample return 0
            return 0
    else:
        return 0  # negative polarity


def label_polarity_all_typs(row, label, column):
    if label in row[column] or label in str(row[column]):  # if type is in current label
        if row['polarity'] == 1:    # and not already a negative sample
            return 1  # positive polarity
        else:   # if already a negative sample return 0
            return 0
    else:
        return 0  # negative polarity


# dictionaries in which to store classifiers, arranges by type/category
classifiers_all_cat = dict.fromkeys(categories)
print('classifiers_all_cat', classifiers_all_cat)

for df in cats_dfs:
    copy_ds = all_samples.copy()
    cat_label = df["category"].unique()
    # print('cat label', cat_label)
    copy_ds["y"] = copy_ds.apply(lambda row: label_polarity(row, cat_label, 'category'), axis=1)    # label +ve and -ve
    train_set = random_sample_ratioed(copy_ds, 0.80, 1, 1)  # split differently according to pos/neg balance
    # X = train_set['concatenated_vector']
    X = train_set['we_np_vector']
    y = train_set["y"]
    classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
    classifiers_all_cat[cat_label[0]] = classifier


# just last (theoretically most fine-grained type)
# for df in types_dfs:
#     copy_ds2 = all_samples.copy()
#     typ_label = df["fine type"].unique()   # get the type associated with this df iteration
#     copy_ds2["y"] = copy_ds2.apply(lambda row: label_polarity(row, typ_label, 'fine type'), axis=1)  # label -/+
#     train_set = random_sample_ratioed(copy_ds2, 0.80, 1, 1)  # split differently according to pos/neg balance
#     # X = train_set['concatenated_vector']
#     X = train_set['we_np_vector']
#     y = train_set["y"]
#     classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
    # classifiers_all_typ[typ_label] = classifier


types_all = set(types_all) # get unique values
print(len(types_all)) # 310 unique types

# dictionaries in which to store classifiers, arranges by type/category
classifiers_all_typ = dict.fromkeys(types)
print('classifiers_all_typ', classifiers_all_typ)


# all types: not just last type
for typ_label in types_all:
    copy_ds2 = all_samples.copy()
    print('type label', typ_label)
    copy_ds2["y"] = copy_ds2.apply(lambda row: label_polarity_all_typs(row, typ_label, 'type'), axis=1)  # label -/+
    train_set = random_sample_ratioed(copy_ds2, 0.80, 1, 1)  # split differently according to pos/neg balance
    # X = train_set['concatenated_vector']
    X = train_set['we_np_vector']
    y = train_set["y"]
    classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
    classifiers_all_typ[typ_label] = classifier


pickl('classifiers_all_cat', classifiers_all_cat)
pickl('classifiers_all_typ',classifiers_all_typ)

