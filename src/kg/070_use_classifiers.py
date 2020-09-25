''' author: Eleanor Bill @eljne '''
''' classify test data '''
import operator
import pandas as pd
import re
import numpy as np
from kg.EB_classes import unpickle, pickl

'''unpickle classifiers'''
classifiers_pos_cat = unpickle('classifiers_pos_cat')
classifiers_pos_typ = unpickle('classifiers_pos_typ')

'''load test data vectors'''
dbpedia_test_final = unpickle('dbpedia_test_final')
test_data = pd.DataFrame(dbpedia_test_final)

'''change depending on vector component to test'''
vector_component = 'we_wh_vector'


# run through classifiers and store scores
def cat_scores(value):
    category_scores = {}
    test = len(value[vector_component])
    if np.isnan(value[vector_component]).any():
        value[vector_component] = np.zeros(300)
    else:
        if test < 300:
            value[vector_component] = np.zeros(300)
        else:
            pass
    for item in classifiers_pos_cat:
        category = item
        c = classifiers_pos_cat[item]
        pred_cat = c.predict_proba([value[vector_component]])[:, 1]
        print('pred_cat', pred_cat)
        # store label and score in dictionary
        category_scores.update({category: pred_cat})
        print('.')
    sorted_cat = sorted(category_scores.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_cat


def typ_scores(value):
    type_scores = {}
    test = len(value[vector_component])
    if np.isnan(value[vector_component]).any():
        value[vector_component] = np.zeros(300)
    else:
        if test < 300:
            value[vector_component] = np.zeros(300)
        else:
            pass
    for item in classifiers_pos_typ:
        typ = item
        c = classifiers_pos_typ[item]
        if c is not None:
            pred_typ = c.predict_proba([value[vector_component]])
            p2 = re.split(' ', str(pred_typ[0]))
            pred_typ = float(p2[1])
        else:
            pred_typ = float(0)
        # store label and score in dictionary
        type_scores.update({typ: pred_typ})
        print('..')
    sorted_typ = sorted(type_scores.items(), key=operator.itemgetter(1), reverse=True)
    sorted_typ_top_ten = list(sorted_typ)[0:9]
    return sorted_typ_top_ten


# test_data['category_scores'] = str(test_data.apply(cat_scores, axis=1))
test_data['type_scores'] = str(test_data.apply(typ_scores, axis=1))

pickl('test_data', test_data)

# for item in test_data.iterrows():
#     print(item)
#     pred_cat = cat_scores(item)
