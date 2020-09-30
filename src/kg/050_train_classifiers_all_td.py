''' author: Eleanor Bill @eljne '''
''' train a MLP model for each category and type '''
import pandas as pd
from kg.EB_classes import unpickle, get_last, pickl, try_to_load_as_pickled_object_or_None
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np

'''change depending on vector component to test'''
vector_component = 'we_nouns_vector'
# we_wh_vector
# we_nouns_vector
# entities_KGE_vector
# we_type_vector
# concatenated_vector

all_td = try_to_load_as_pickled_object_or_None('data/training_vectors/32_all_td_justconcat') # for using the concatenated vector
# all_td = unpickle('training_vectors/31_all_td_fin') # use all training data
all_samples = pd.DataFrame(all_td)

'''split on types/categories again'''
categories = all_samples['category'].unique()
all_samples['fine type'] = all_samples['type'].apply(get_last)
types = all_samples['fine type'].unique()

# lists to store the dataframes in
types_dfs = [pd.DataFrame(y) for x, y in all_samples.groupby('fine type', as_index=False)] # just last type
cats_dfs = [pd.DataFrame(b) for a, b in all_samples.groupby('category', as_index=False)]
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
all_samples['type'].apply(get_all)
types_all_unique = list(set(types_all)) # make unique

# dictionaries in which to store classifiers, arranges by type/category
classifiers_all_cat = dict.fromkeys(categories)
print('classifiers_all_cat', classifiers_all_cat)
classifiers_all_typ = dict.fromkeys(types_all_unique)
print('classifiers_all_typ', classifiers_all_typ)


def random_sample_ratioed(datafrm, pos_fraction, ratio_pos, ratio_neg):
    # fraction is a ratio e.g.
    positive = datafrm[datafrm['y'] == "1"]
    negative = datafrm[datafrm['y'] == "0"]
    # print('len pos', len(positive))
    # print('len neg', len(negative))
    positive_smples = positive.sample(frac=pos_fraction, random_state=0)
    neg_samples_wanted = ((len(positive_smples) / ratio_pos) * ratio_neg)   # work out number of negative samples we need
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


def train_classifier(train, label):
    parameter_space = {
        'hidden_layer_sizes': [(50, 50, 50), (50, 100, 50), (100,)],
        'activation': ['tanh', 'relu'],
        'solver': ['sgd', 'adam'],
        'alpha': [0.0001, 0.05],
        'learning_rate': ['constant', 'adaptive'],
    }
    train = np.array(list(train))
    mlp = MLPClassifier(max_iter=100)
    clf = GridSearchCV(mlp, parameter_space, n_jobs=-1, cv=3)
    clf.fit(train, label)
    return clf


''' train and store classifiers '''
# categories
for df in cats_dfs:
    copy_df = all_samples.copy()
    cat_label = df["category"].unique()
    cat_label = cat_label[0]
    copy_df["y"] = copy_df.apply(lambda row: label_polarity(row, cat_label, "category"), axis=1)    # label +ve and -ve
    train_set = random_sample_ratioed(copy_df, 0.80, 1, 1)  # split differently according to pos/neg balance
    X = train_set[vector_component]
    y = train_set["y"]
    classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
    classifiers_all_cat[cat_label] = classifier


# all types
for typ_label in types_all_unique:
    copy_df2 = all_samples.copy()
    print('type label', typ_label)
    copy_df2["y"] = copy_df2.apply(lambda row: label_polarity_all_typs(row, typ_label, 'type'), axis=1)  # label -/+
    train_set = random_sample_ratioed(copy_df2, 0.80, 1, 1)  # split differently according to pos/neg balance
    X = train_set[vector_component]
    y = train_set["y"]
    classifier = train_classifier(X, y)  # need to convert vector from list of arrays to matrix
    classifiers_all_typ[typ_label] = classifier

print('classifiers_all_cat', classifiers_all_cat)
pickl('classifiers/classifiers_all_cat_ALL', classifiers_all_cat)

print('classifiers_all_typ', classifiers_all_typ)
pickl('classifiers/classifiers_all_typ_ALL', classifiers_all_typ)

