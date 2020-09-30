from kg.EB_classes import unpickle
import re

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
results['types'] = results.apply(get_first_list, axis=1)

results2 = results[['id', 'category', 'types']]
results_dict = results2.to_dict('records')
print(results_dict)
results2.to_json(r'data/results/for_evaluation/system_output_json.json')