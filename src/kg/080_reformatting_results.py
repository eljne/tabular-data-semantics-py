from kg.EB_classes import unpickle
import csv

# results_OGTD = unpickle('results/results_OGTD')
results = unpickle('results/results_ALLTD')

# results_OGTD = results_OGTD['type_scores']
# results = results_ALLTD['type_scores']

''' REFORMATTING FOR EVAL SCRIPT '''
''' export results to be used in evaluation script '''

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