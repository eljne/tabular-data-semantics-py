''' author: Eleanor Bill @eljne '''
''' classify test data '''
import operator
import pandas as pd
import csv
from kg.EB_classes import unpickle

'''unpickle classifiers'''
classifiers_all_cat = unpickle('classifiers_all_cat')
classifiers_all_typ = unpickle('classifiers_all_typ')

'''load test data vectors'''
dbpedia_test_final = unpickle('dbpedia_test_final')
test_data = pd.DataFrame(dbpedia_test_final)

''' run through classifiers and store scores'''
category_scores = {}
type_scores = {}

all_cat = []
all_typ = []

'''category'''
for value in test_data:
    question = value['question']
    for c, category in classifiers_all_cat:
        pred_cat = c.predict([value['concatenated vector']])
        # store label and score in dictionary
        category_scores.update({category: pred_cat})
    all_cat.append([question, category_scores])
results_cat = []
for question, value in all_cat:
    sorted_cat = sorted(value.items(), key=operator.itemgetter(1))
    results_cat.append([question, sorted_cat])

'''type'''
for value in test_data:
    question = value['question']
    for c, typ in classifiers_all_typ:
        pred_typ = c.predict([value['concatenated vector']])
        # store label and score in dictionary
        type_scores.update({type: pred_typ})
    all_typ.append([question, type_scores])
results_typ = []
for question, value in all_typ:
    sorted_typ = sorted(value.items(), key=operator.itemgetter(1))
    sorted_typ_top_ten = sorted_typ[0:9]
    results_typ.append([question, sorted_typ_top_ten])

# convert to dataframe and join on question?
df_results_typ = pd.DataFrame(results_typ)
df_results_cat = pd.DataFrame(results_cat)

results = df_results_typ.set_index('question').join(df_results_cat.set_index('question'))
# sorted_x.reverse()

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