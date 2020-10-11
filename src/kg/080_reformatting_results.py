''' author: Eleanor Bill @eljne '''
''' reformats results to be run through evaluation script'''

from kg.EB_classes import unpickle, heuristics_2
import re
import json

# results = unpickle('results/results_OGTD')

results = unpickle('results/results_ALLTD')

''' REFORMATTING FOR EVAL SCRIPT '''
''' export results to be used in evaluation script '''

'''    - `system_output_json` is a JSON file with the (participating) system's
      category and type predictions. The format is a list of dictionaries with
      keys `id`, `category`, and `type`, holding the question ID, predicted
      category, and ranked list of up to 10 types, respectively.'''


def get_first(value):
    val = value['category_scores']
    val = val.split(',')
    val = val[0]
    re.sub('[^A-Za-z0-9]+', '', val)
    val = val.replace("'", "")
    val = val.replace("(", "")
    return str(val)


def get_first_list(value):
    val_list = []
    val = value['type_scores']
    val = val.split(',')
    for v in val:
        re.sub('[^A-Za-z0-9]+', '', v)
        v = v.replace("'", "")
        v = v.replace("(", "")
        v = v.replace(")", "")
        v = v.replace("[", "")
        v = v.replace("]", "")
        v = v.replace(".", "")
        v = v.replace(" ", "")
        for i in range(10):
            v = v.replace(str(i), '')
        if v != '':
            val_list.append(v)
    return val_list


results['category'] = results.apply(get_first, axis=1)
results['type'] = results.apply(get_first_list, axis=1)
results = results.apply(heuristics_2, axis=1)
# print(results['question'])
results = results[['id', 'category', 'type', 'question', 'wh']]
results_list = []


def reform(value):
    i = value['id']
    c = value['category']
    t = value['type']
    q = value['question']
    wh = value['wh']
    dict = {"id": i, "category": c, "type": t}
    # dict = {"category": c, 'wh': wh, "question": q}
    results_list.append(dict)
    print(dict)
    return 0


results.apply(reform, axis=1)
json_string = json.dumps(results_list)

with open('data/results/for_evaluation/system_output_json.json', 'w') as write_file:
    write_file.write(json_string)
