''' author: Eleanor Bill @eljne '''
''' classify test data '''
import operator
import pandas as pd
from kg.EB_classes import unpickle, pickl, heuristics, replace_Location
from kg.EB_classes import reformat, reformat_2, reformat_3, reformat_4, reformat_5, reformat_6
import re

'''change depending on vector component to test'''
vector_component_category = 'concatenated_vector'
vector_component_type = 'concatenated_vector'
# we_wh_vector
# we_nouns_vector
# entities_KGE_vector
# we_type_vector
# con_wh_nouns
# con_wh_kge
# con_nouns_KGE
# con_wh_nouns_kge
# con_wh_kge_types
# concatenated_vector

'''unpickle classifiers'''
# use classifiers trained on all training data
classifiers_cat = unpickle('classifiers/classifiers_all_cat_ALL')
classifiers_typ = unpickle('classifiers/classifiers_all_typ_ALL')
results_path = 'results/results_ALLTD'

# use classifiers trained on original training data
# classifiers_cat = unpickle('classifiers/classifiers_all_cat_OGTD')
# classifiers_typ = unpickle('classifiers/classifiers_all_typ_OGTD')
# results_path = 'results/results_OGTD'

'''load test data vectors'''
# dbpedia_test_final = unpickle('testing_vectors/10_dbpedia_test_fin')    # when using provided by task
dbpedia_test_final = unpickle('testing_vectors/11_testing_vectors_from_og_training_data')  # when using og training
test_data = pd.DataFrame(dbpedia_test_final)    # data split

# test_data['con_wh_nouns_2'] = test_data.apply(reformat_2, axis=1)
# test_data2 = test_data.drop(['con_wh_nouns'], axis=1)
# test_data = test_data2.rename(columns={'con_wh_nouns_2': 'con_wh_nouns'})

# test_data['con_wh_kge_2'] = test_data.apply(reformat_3, axis=1)
# test_data2 = test_data.drop(['con_wh_kge'], axis=1)
# test_data = test_data2.rename(columns={'con_wh_kge_2': 'con_wh_kge'})

# test_data['con_nouns_KGE_2'] = test_data.apply(reformat_4, axis=1)
# test_data2 = test_data.drop(['con_nouns_KGE'], axis=1)
# test_data = test_data2.rename(columns={'con_nouns_KGE_2': 'con_nouns_KGE'})

# test_data['con_wh_nouns_kge_2'] = test_data.apply(reformat_5, axis=1)
# test_data2 = test_data.drop(['con_wh_nouns_kge'], axis=1)
# test_data = test_data2.rename(columns={'con_wh_nouns_kge_2': 'con_wh_nouns_kge'})

# test_data['con_wh_kge_types_2'] = test_data.apply(reformat_6, axis=1)
# test_data2 = test_data.drop(['con_wh_kge_types'], axis=1)
# test_data = test_data2.rename(columns={'con_wh_kge_types_2': 'con_wh_kge_types'})

test_data['concatenated_vector_2'] = test_data.apply(reformat, axis=1)
test_data2 = test_data.drop(['concatenated_vector'], axis=1)
test_data = test_data2.rename(columns={'concatenated_vector_2': 'concatenated_vector'})

print('done reformat cc v')

'''run through classifiers and store scores'''


def cat_scores(value):
    category_scores = {}
    test = value[vector_component_category]
    wh = value['wh']
    predict = list(test)
    for item in classifiers_cat:  # for each classifier
        category = item  # get category
        c = classifiers_cat[item]  # get classifier
        pred_cat = c.predict_proba([predict])  # use vector component and classifier to predict
        p2 = re.split(' ', str(pred_cat[0]))  # get probability of it being that class
        try:
            pred_cat = float(p2[1])
        except:
            pred_cat = 0.00000000
        category_scores.update({category: pred_cat})  # store label and score in dictionary
    sorted_cat = heuristics(category_scores, wh, 'category')
    sorted_cat2 = sorted(sorted_cat.items(), key=operator.itemgetter(1), reverse=True)
    sorted_cat_top = list(sorted_cat2)[0]
    print('.')
    return str(sorted_cat_top)


def typ_scores(value):
    type_scores = {}
    test = value[vector_component_type]
    wh = value['wh']
    predict = list(test)
    for item in classifiers_typ:  # for each classifier
        typ = item  # get type
        c = classifiers_typ[item]  # get classifier
        pred_typ = c.predict_proba([predict])
        p2 = re.split(' ', str(pred_typ[0]))
        try:
            pred_typ = float(p2[1])
        except:
            pred_typ = 0.00000000
        type_scores.update({typ: pred_typ})  # store label and score in dictionary
    sorted_typ = heuristics(type_scores, wh, 'type')
    sorted_typ2 = sorted(sorted_typ.items(), key=operator.itemgetter(1), reverse=True)
    sorted_typ3 = replace_Location(list(sorted_typ2))
    sorted_typ_top_ten = sorted_typ3[0:10]
    print('..')
    return str(sorted_typ_top_ten)


test_data = test_data.drop_duplicates(subset=['id'])
test_data['category_scores'] = test_data.apply(cat_scores, axis=1)
test_data['type_scores'] = test_data.apply(typ_scores, axis=1)
pickl(results_path, test_data)
