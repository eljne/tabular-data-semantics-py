from kg.EB_classes import unpickle
import csv

results_OGTD = unpickle('results/results_OGTD')
results_ALLTD = unpickle('results/results_ALLTD')

results_OGTD = results_OGTD['type_scores']
results_ALL = results_ALLTD['type_scores']

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