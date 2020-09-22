''' author: Eleanor Bill @eljne '''
''' calls pre-written evaluation script and returns accuracy/KPIs '''

from kg.evaluation_code import main

'''
Where
    - `type_hierarchy_tsv` is a TSV file with Type, Depth and Parent columns.
      The file is assumed to contain a header row.
    - `ground_truth_json` is a JSON file containing the input questions and the
      ground truth category and list of types (following the format of the
      training data files).
    - `system_output_json` is a JSON file with the (participating) system's
      category and type predictions. The format is a list of dictionaries with
      keys `id`, `category`, and `type`, holding the question ID, predicted
      category, and ranked list of up to 10 types, respectively.
'''

type_hierarchy_tsv = 'data/type_hierarchy_tsv.tsv'
ground_truth_json = 'data/ground_truth_json.json'
system_output_json = 'data/system_output_json.json'

# should print results in terminal
main(type_hierarchy_tsv, ground_truth_json, system_output_json)