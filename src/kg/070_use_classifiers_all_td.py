''' author: Eleanor Bill @eljne '''
''' classify test data '''
import operator
import numpy as np
import pandas as pd
from kg.EB_classes import unpickle, pickl
import re

'''change depending on vector component to test'''
vector_component = 'we_nouns_vector'
# we_wh_vector
# we_nouns_vector
# entities_KGE_vector
# we_type_vector
# concatenated_vector

'''unpickle classifiers'''
classifiers_all_cat = unpickle('classifiers/classifiers_all_cat_ALL')
classifiers_all_typ = unpickle('classifiers/classifiers_all_typ_ALL')

'''load test data vectors'''
dbpedia_test_final = unpickle('testing_vectors/11_dbpedia_test_fin')
test_data = pd.DataFrame(dbpedia_test_final)

''' run through classifiers and store scores'''


def reformat(row_column):
    concatenated_vector_2 = []
    for component in row_column:
        component_list = component.tolist()
        concatenated_vector_2.append(component_list)
    return concatenated_vector_2


# run through classifiers and store scores
def cat_scores(value):
    category_scores = {}
    predict = reformat(value[vector_component])
    for item in classifiers_all_cat:    # for each classifier
        category = item # get category
        c = classifiers_all_cat[item]   # get classifier
        pred_cat = c.predict_proba([predict])   # use vector component and classifier to predict
        p2 = re.split(' ', str(pred_cat[0]))    # get probability of it being that class
        pred_cat = float(p2[1])
        category_scores.update({category: pred_cat})    # store label and score in dictionary
    sorted_cat = sorted(category_scores.items(), key=operator.itemgetter(1), reverse=True)
    sorted_cat_top = list(sorted_cat)[0]
    print('.')
    return str(sorted_cat_top)


def typ_scores(value):
    type_scores = {}
    # predict = reformat(value[vector_component])
    predict = np.random.rand(300)
    # print([predict])    # always different
    for item in classifiers_all_typ:    # for each classifier
        typ = item  # get type
        c = classifiers_all_typ[item]   # get classifier
        pred_typ = c.predict_proba([predict])
        p2 = re.split(' ', str(pred_typ[0]))
        pred_typ = float(p2[1])
        type_scores.update({typ: pred_typ})  # store label and score in dictionary
    sorted_typ = sorted(type_scores.items(), key=operator.itemgetter(1), reverse=True)
    sorted_typ_top_ten = list(sorted_typ)[0:9]
    print('..')
    return str(sorted_typ_top_ten)


test_data = test_data.drop_duplicates(subset=['id'])
test_data['category_scores'] = test_data.apply(cat_scores, axis=1)
test_data['type_scores'] = test_data.apply(typ_scores, axis=1)
pickl('results/results_ALLTD', test_data)