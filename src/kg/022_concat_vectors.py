# Eleanor Bill 4 September 2020
# concatenate vectors and export to dataframe/csv

import pickle
import pandas as pd

pkl_file = open('data/dbpedia_train_all_vectors.pkl', 'rb')
dbpedia_train_wh = pickle.load(pkl_file)
pkl_file.close()

'''
we_wh_vector - First position could be for the embedding of the wh question word (we can create our own embedding/encoding).
we_nouns_vector - Second position for the WE of the sentence or set of nouns.
we_np_vector - Third position (up to 3 or 4 vector positions? we can play with different values) for noun phrases without a good correspondence in KG (WE of the noun phrase)
entities_KGE_vector - Fourth position (up to 3 or 4 vector positions) for noun phrases with a good correspondence in KG (KGE of entity representing noun phrase)
we_type_vector - Fifth position (up to 3 or 4 vector positions) for the WE of the types of the KG entities above.
'''


def write_file(file_to_write, filename):
    myFile = open('data/' + filename + '.txt', 'w')
    myFile.write(str(file_to_write))
    myFile.write('\n')
    myFile.close()
    return 0


def concatenate_vector(entry):
    cv = [entry['we_wh_vector'],
          entry['we_nouns_vector'],
          entry['we_np_vector'],
          entry['entities_KGE_vector'],
          entry['we_type_vector']]
    return cv


re_list = []
for entry in dbpedia_train_wh:
    concatenated_vector = concatenate_vector(entry)
    entry.update({'concatenated_vector': concatenated_vector})
    re_list.append(entry)

print('done concatenate vector')
dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '12_dbpedia_train_wh')

# pickle
f = open('data/df.pkl', 'wb')
pickle.dump(dbpedia_train_wh, f)
f.close()