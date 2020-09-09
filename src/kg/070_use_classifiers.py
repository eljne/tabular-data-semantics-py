''' classify test data '''
import pickle
import pandas as pd
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
        pred = c.predict([value])
        if pred > max_pos:
            max_neg = pred
            best_pos_cat = c

max_neg = 0
for value in test_data:
    for c in classifiers_all_cat:
        pred = c.predict([value])
        if pred > max_neg:
            max_neg = pred
            best_all_cat = c


'''type'''
max_pos = 0
for value in test_data:
    for c in classifiers_pos_type:
        pred = c.predict([value])
        if pred > max_pos:
            max_neg = pred
            best_pos_typ = c

max_neg = 0
for value in test_data:
    for c in classifiers_all_type:
        pred = c.predict([value])
        if pred > max_neg:
            max_neg = pred
            best_all_type = c