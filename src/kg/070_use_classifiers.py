''' author: Eleanor Bill @eljne '''
''' classify test data '''

import pickle
import pandas as pd
import csv
from sklearn.neural_network import MLPClassifier

'''unpickle classifiers'''

pkl_file = open('data/classifiers_pos_cat.pkl', 'rb')
classifiers_pos_cat = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('data/classifiers_pos_typ.pkl', 'rb')
classifiers_pos_typ = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('data/classifiers_all_cat.pkl', 'rb')
classifiers_all_cat = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('data/classifiers_all_typ.pkl', 'rb')
classifiers_all_typ = pickle.load(pkl_file)
pkl_file.close()


'''load test data vectors'''

pkl_file = open('data/dbpedia_test_final.pkl', 'rb')
dbpedia_test_final = pickle.load(pkl_file)
pkl_file.close()
test_data = pd.DataFrame(dbpedia_test_final)

''' run through classifiers '''

'''category'''
max_pos = 0
for value in test_data:
    for c in classifiers_pos_cat:
        pred = c.predict([value['concatenated vector']])
        if pred > max_pos:
            max_neg = pred
            best_pos_cat = c

max_neg = 0
for value in test_data:
    for c in classifiers_all_cat:
        pred = c.predict([value['concatenated vector']])
        if pred > max_neg:
            max_neg = pred
            best_all_cat = c


'''type'''
max_pos = 0
for value in test_data:
    for c in classifiers_pos_type:
        pred = c.predict([value['concatenated vector']])
        if pred > max_pos:
            max_neg = pred
            best_pos_typ = c

max_neg = 0
for value in test_data:
    for c in classifiers_all_type:
        pred = c.predict([value['concatenated vector']])
        if pred > max_neg:
            max_neg = pred
            best_all_type = c


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