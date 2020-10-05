''' author: Eleanor Bill @eljne '''
''' reformat test data to evaluate '''

from kg.EB_classes import unpickle, replace_Location_2
import json
import pandas as pd

test_truth = unpickle('testing_vectors/11_testing_vectors_from_og_training_data')
test_truth = pd.DataFrame(test_truth)

test_truth['type2'] = test_truth['type'].apply(replace_Location_2)
test_truth2 = test_truth.drop(['type'], axis=1)
test_truth3 = test_truth2.rename(columns={'type2': 'type'})
test_truth3 = test_truth3[['question', 'category', 'type', 'id']]
test_truth_json = []


def reform(value):
    i = value['id']
    c = value['category']
    t = value['type']
    q = value['question']
    dict = {"id": i, "category": c, "type": t, "question": q}
    print(dict)
    test_truth_json.append(dict)
    return 0


test_truth3.apply(reform, axis=1)
json_string = json.dumps(test_truth_json)

with open('data/results/for_evaluation/ground_truth_json.json', 'w') as write_file:
    write_file.write(json_string)

'''in terminal use: python evaluate.py type_hierarchy_tsv.tsv ground_truth_json.json system_output_json.json'''