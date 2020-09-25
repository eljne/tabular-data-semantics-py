''' author: Eleanor Bill @eljne '''
''' classify test data '''
import operator
import pandas as pd
import csv
import numpy as np
from kg.EB_classes import unpickle

'''unpickle classifiers'''
classifiers_pos_cat = unpickle('classifiers_pos_cat')
classifiers_pos_typ = unpickle('classifiers_pos_typ')

'''load test data vectors'''
dbpedia_test_final = unpickle('dbpedia_test_final')
test_data = pd.DataFrame(dbpedia_test_final)

vector_component = 'we_wh_vector'

''' run through classifiers and store scores'''

# for item in classifiers_pos_cat:
#     print("Key : {} , Value : {}".format(item, classifiers_pos_cat[item]))


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
        pred_cat = c.predict([value[vector_component]])
        # store label and score in dictionary
        category_scores.update({category: pred_cat})
        sorted_cat = sorted(category_scores.items(), key=operator.itemgetter(1))
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
        try:
            pred_typ = c.predict([value[vector_component]])
        except:
            pred_typ = 0
        # store label and score in dictionary
        type_scores.update({typ: pred_typ})
        sorted_typ = sorted(type_scores.items(), key=operator.itemgetter(1))
        sorted_typ_top_ten = list(sorted_typ)[0:9]
    return sorted_typ_top_ten


test_data['category_scores'] = str(test_data.apply(cat_scores, axis=1))
test_data['type_scores'] = str(test_data.apply(typ_scores, axis=1))

# for item in test_data.iterrows():
#     print(item)
#     pred_cat = cat_scores(item)

results = test_data['type_scores']

''' REFORMATTING FOR EVAL SCRIPT '''
''' export results to be used in evaluation script '''

'''    - `type_hierarchy_tsv` is a TSV file with Type, Depth and Parent columns.
      The file is assumed to contain a header row.'''

with open("data/type_hierarchy_tsv.tsv", "w") as fd:
    writer = csv.DictWriter(fd, dialect="excel-tab", fieldnames=field_names)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

'''    - `ground_truth_json` is a JSON file containing the input questions and the
      ground truth category and list of types (following the format of the
      training data files).'''

results = results[results['question', 'category', 'types']]
results.to_json(r'data/ground_truth_json.json')

'''    - `system_output_json` is a JSON file with the (participating) system's
      category and type predictions. The format is a list of dictionaries with
      keys `id`, `category`, and `type`, holding the question ID, predicted
      category, and ranked list of up to 10 types, respectively.'''

results = results[results['id', 'category', 'type']]
results.to_json(r'data/ground_truth_json.json')