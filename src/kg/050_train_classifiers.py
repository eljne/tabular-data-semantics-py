''' author: Eleanor Bill @eljne '''
''' train a MLP model for each category and type '''
import pandas as pd
from kg.EB_classes import unpickle, get_last, pickl
from kg.EB_classes import reformat, reformat_2, reformat_3, reformat_4, reformat_5, reformat_6
from sklearn.neural_network import MLPClassifier
import numpy as np


'''change depending on vector component to test'''
vector_component_category = 'con_wh_nouns'
vector_component_type = 'con_wh_nouns'
# we_wh_vector
# we_nouns_vector
# entities_KGE_vector
# we_type_vector
# concatenated_vector
# con_wh_nouns
# con_wh_kge
# con_nouns_KGE
# con_wh_nouns_kge
# con_wh_kge_types

'''load training data'''
# use all training data
file_path_cat = 'classifiers/classifiers_all_cat_ALL'
file_path_typ = 'classifiers/classifiers_all_typ_ALL'
all_td = unpickle('training_vectors/31_all_td_fin') # use all training data
td = pd.DataFrame(all_td)

# use only original training data
# file_path_cat = 'classifiers/classifiers_all_cat_OGTD'
# file_path_typ = 'classifiers/classifiers_all_typ_OGTD'
# og_td = unpickle('training_vectors/final_original_training_vectors')
# td = pd.DataFrame(og_td)
# td['polarity'] = "1"

td['concatenated_vector_2'] = td.apply(reformat, axis=1)
td2 = td.drop(['concatenated_vector'], axis=1)
td = td2.rename(columns={'concatenated_vector_2': 'concatenated_vector'})

td['con_wh_nouns_2'] = td.apply(reformat_2, axis=1)
td2 = td.drop(['con_wh_nouns'], axis=1)
td = td2.rename(columns={'con_wh_nouns_2': 'con_wh_nouns'})

td['con_wh_kge_2'] = td.apply(reformat_3, axis=1)
td2 = td.drop(['con_wh_kge'], axis=1)
td = td2.rename(columns={'con_wh_kge_2': 'con_wh_kge'})

td['con_nouns_KGE_2'] = td.apply(reformat_4, axis=1)
td2 = td.drop(['con_nouns_KGE'], axis=1)
td = td2.rename(columns={'con_nouns_KGE_2': 'con_nouns_KGE'})

td['con_wh_nouns_kge_2'] = td.apply(reformat_5, axis=1)
td2 = td.drop(['con_wh_nouns_kge'], axis=1)
td = td2.rename(columns={'con_wh_nouns_kge_2': 'con_wh_nouns_kge'})

td['con_wh_kge_types_2'] = td.apply(reformat_6, axis=1)
td2 = td.drop(['con_wh_kge_types'], axis=1)
training_data = td2.rename(columns={'con_wh_kge_types_2': 'con_wh_kge_types'})

print('done reformat cc v')


'''split on types/categories again'''
categories = training_data['category'].unique()
training_data['fine type'] = training_data['type'].apply(get_last)
types = training_data['fine type'].unique()

# lists to store the dataframes in
types_dfs = [pd.DataFrame(y) for x, y in training_data.groupby('fine type', as_index=False)] # just last type
cats_dfs = [pd.DataFrame(b) for a, b in training_data.groupby('category', as_index=False)]
print('done split to types and categories')


# get all relevant types from list of them
def get_all(list):
    for t in list:
        if t.startswith('dbo:'):
            types_all.append(t)
        else:
            pass
    return 0


# get list of all types
types_all = []
training_data['type'].apply(get_all)
types_all_unique = list(set(types_all)) # make unique

# dictionaries in which to store classifiers, arranges by type/category
classifiers_cat = dict.fromkeys(categories)
print('classifiers_all_cat', classifiers_cat)
classifiers_typ = dict.fromkeys(types_all_unique)
print('classifiers_all_typ', classifiers_typ)


def random_sample_ratioed(datafrm, pos_fraction, ratio_pos, ratio_neg):
    # fraction is a ratio e.g.
    positive = datafrm[datafrm['y'] == "1"]
    negative = datafrm[datafrm['y'] == "0"]
    positive_smples = positive.sample(frac=pos_fraction, random_state=0)
    neg_samples_wanted = ((len(positive_smples) / ratio_pos) * ratio_neg)   # work out number of negative samples we need
    fraction2 = neg_samples_wanted / len(negative)
    try:
        negative_smples = negative.sample(frac=fraction2, random_state=0)
    except:
        print('not enough negative data, try diff ratio/fraction')
        return pd.DataFrame()
    new_df = pd.concat([positive_smples, negative_smples])  # append all data together
    new_df2 = new_df.sample(frac=1)  # shuffle dataframe
    return new_df2


# choose the number of negative examples trained for each positive example

def label_polarity(row, label, column):
    if row[column] == label or str(row[column]) == label: # if type/category is current label
        if row['polarity'] == 1 or row['polarity'] == "1":    # and not already a negative sample
            return "1"  # positive polarity
        else:   # if already a negative sample return 0
            return "0"
    else:
        return "0"  # negative polarity


def label_polarity_all_typs(row, label, column):
    if label == str(row[column]) or label in str(row[column]):  # if type is in current label
        if row['polarity'] == 1 or row['polarity'] == "1":    # and not already a negative sample
            return "1"  # positive polarity
        else:   # if already a negative sample return 0
            return "0"
    else:
        return "0"  # negative polarity


def train_classifier_category(train, label):
    training_data = np.array(list(train))
    print('category train')
    clf = MLPClassifier(max_iter=300)
    clf.fit(training_data, label)
    print('category training complete')
    return clf


def train_classifier(train, label):
    training_data = np.array(list(train))
    print('type train')
    clf = MLPClassifier(max_iter=300)
    clf.fit(training_data, label)
    print('type training complete')
    return clf


''' train and store classifiers '''
# categories
for df in cats_dfs:
    copy_df = training_data.copy()
    cat_label = df["category"].unique()
    cat_label = cat_label[0]
    copy_df["y"] = copy_df.apply(lambda row: label_polarity(row, cat_label, "category"), axis=1)    # label +ve and -ve
    train_set = random_sample_ratioed(copy_df, 0.80, 1, 1)  # split differently according to pos/neg balance
    X = train_set[vector_component_category]
    y = train_set["y"]
    classifier = train_classifier_category(X, y)  # need to convert vector from list of arrays to matrix
    classifiers_cat[cat_label] = classifier


# all types
for typ_label in types_all_unique:
    copy_df2 = training_data.copy()
    print('type label', typ_label)
    copy_df2["y"] = copy_df2.apply(lambda row: label_polarity_all_typs(row, typ_label, 'type'), axis=1)  # label -/+
    train_set = random_sample_ratioed(copy_df2, 0.80, 1, 1)  # split differently according to pos/neg balance
    X = train_set[vector_component_type]
    y = train_set["y"]
    classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
    classifiers_typ[typ_label] = classifier

print('classifiers_cat', classifiers_cat)
pickl(file_path_cat, classifiers_cat)

print('classifiers_typ', classifiers_typ)
pickl(file_path_typ, classifiers_typ)

