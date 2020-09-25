''' author: Eleanor Bill @eljne '''
''' train a MLP model for each category and type: only use initial training data'''

import pandas as pd
from kg.EB_classes import unpickle, get_last_2, pickl
from sklearn.neural_network import MLPClassifier

# use only original training data
load = unpickle('df')
positive_samples = pd.DataFrame(load)
# print(positive_samples.head)

vector_component = 'we_wh_vector'

'''split on types/categories again'''

# def unique_array_workaround(series):
#     series2 = []
#     for item in series:
#         item2 = str(item)
#         if item2 != '[]' and item2 != []:   # get rid of label = []
#             series2.append(item2)
#     ty = list(set(series2))
#     return ty


categories = positive_samples['category'].unique()
positive_samples['fine type'] = positive_samples['type'].apply(get_last_2)
types = positive_samples['fine type'].unique()

types_dfs = [pd.DataFrame(y) for x, y in positive_samples.groupby('fine type', as_index=False)]  # just last one
cats_dfs = [pd.DataFrame(y) for x, y in positive_samples.groupby('category', as_index=False)]

print('done split to types and categories')


def get_all(list):
    for t in list:
        types_all.append(t)
    return 0


# all types
types_all = []
positive_samples['type'].apply(get_all)
types_all_unique = list(set(types_all))
print('all types', types_all_unique)


# select positive samples at random from training data
def random_sample_ratioed(datafrm, pos_fraction, ratio_pos, ratio_neg):
    positive = datafrm[datafrm['y'] == 1]  # get positive data
    negative = datafrm[datafrm['y'] == 0]  # get negative data
    # find out how much +ve data we have, how much -ve we want
    positive_smples = positive.sample(frac=pos_fraction, random_state=0)
    neg_samples_wanted = ((len(positive_smples) / ratio_pos) * ratio_neg)
    fraction2 = neg_samples_wanted / len(negative)
    try:
        negative_smples = negative.sample(frac=fraction2, random_state=0)
    except:
        print('not enough negative data, try diff ratio/fraction')
        return pd.DataFrame()
    print('positive samples length', len(positive_smples))
    print('negative samples length', len(negative_smples))
    new_df = pd.concat([positive_smples, negative_smples])  # append all data together
    new_df2 = new_df.sample(frac=1)  # shuffle dataframe
    return new_df2


# trains MLP classifier
def train_classifier(train, label):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(list(train), label)  # debug from here
    return clf


# assigns polarity based on given category/type
def label_polarity(row, label, column):
    if row[column] == label or str(row[column]) == label:  # if type/category is current label
        return 1  # positive polarity
    else:
        return 0  # negative polarity


# same as above except with strings
def label_polarity_all_typs(row, label, column):
    if label in row[column] or label in str(row[column]):  # if type is in current label
        return 1  # positive polarity
    else:
        return 0  # negative polarity


'''categories'''
# dictionaries in which to store classifiers, arranges by type/category
classifiers_pos_cat = dict.fromkeys(categories)
print('classifiers_pos_cat', classifiers_pos_cat)

# iterate through categories, get training data, train classifiers, store classifiers
for df in cats_dfs:
    copy_ds = positive_samples.copy()
    cat_label = df["category"].unique()
    # print('cat label', cat_label)
    copy_ds["y"] = copy_ds.apply(lambda row: label_polarity(row, cat_label, 'category'), axis=1)  # label +ve and -ve
    train_set = random_sample_ratioed(copy_ds, 0.80, 1, 1)  # split differently according to pos/neg balance
    # X = train_set['concatenated_vector']
    X = train_set[vector_component]
    y = train_set["y"]
    classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
    classifiers_pos_cat[cat_label[0]] = classifier
    print('.')

'''types'''
types_all = set(types_all)  # get unique values
print(len(types_all))  # 310 unique types

# dictionaries in which to store classifiers, arranges by type/category
classifiers_pos_typ = dict.fromkeys(types_all)
print('classifiers_pos_typ', classifiers_pos_typ)

# just last (theoretically most fine-grained type)
# for df in types_dfs:
#     copy_ds2 = positive_samples.copy()
#     typ_label = df["fine type"].unique()  # get the type associated with this df iteration
#     copy_ds2["y"] = copy_ds2.apply(lambda row: label_polarity(row, typ_label, 'fine type'), axis=1)  # label -/+
#     train_set = random_sample_ratioed(copy_ds2, 0.80, 1, 1)  # split differently according to pos/neg balance
#     X = train_set[vector_component]
#     y = train_set["y"]
#     classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
#     classifiers_pos_typ[typ_label[0]] = classifier
#     print('..')

# all types: not just last type
for typ_label in types_all:
    copy_ds2 = positive_samples.copy()
    print('type label', typ_label)
    copy_ds2["y"] = copy_ds2.apply(lambda row: label_polarity_all_typs(row, typ_label, 'type'), axis=1)  # label -/+
    train_set = random_sample_ratioed(copy_ds2, 0.80, 1, 1)  # split differently according to pos/neg balance
    # X = train_set['concatenated_vector']
    X = train_set[vector_component]
    y = train_set["y"]
    classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
    print(classifier)
    classifiers_pos_typ[typ_label[0]] = classifier

pickl('classifiers_pos_cat', classifiers_pos_cat)
pickl('classifiers_pos_typ', classifiers_pos_typ)
print('done pickled')
