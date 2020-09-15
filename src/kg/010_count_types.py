# load json files
# find category and type in training data
# save question data to be parsed
# count types in training data and save in file
# Eleanor Bill finished 12th August 2020

import json
from kg.EB_classes import load_json, write_file


def write_file_it(file_to_write, filename):
    myFile = open('data/' + filename + '.txt', 'w')
    for element in file_to_write:
        myFile.write(str(element))
        myFile.write('\n')
    myFile.close()
    return 0


def count_it(lst):
    counts = dict()
    for i in lst:
        try:
            counts[i] = counts.get(i, 0) + 1
        except Exception as e:
            print(e)
    return counts


# to dictionary
dbpedia_train = load_json("data/smarttask_dbpedia_train")

'''find out the answer types in the training data'''

db_arr_cat = []  # lists of categories and types
db_arr_type = []
db_arr_q = []
for a in dbpedia_train: # append
    db_arr_cat.append(a['category'])
    db_arr_type.append(a['type'])
    db_arr_q.append(a['question'])
    # print(a)


db_arr_type_coarse = []
db_arr_type_fine = []

# flatten category data into single list
db_arr_type2 = [item for sublist in db_arr_type for item in sublist]

# remove empty
db_arr_type = [x for x in db_arr_type if x]

for i in db_arr_type:
    db_arr_type_coarse.append(i[-1])

for i in db_arr_type:
    db_arr_type_fine = list(set(db_arr_type2) - set(db_arr_type_coarse))

# save data in files
write_file_it(db_arr_cat, 'db_arr_cat')
write_file_it(db_arr_type, 'db_arr_type')
write_file_it(db_arr_type2, 'db_arr_type2')
write_file_it(db_arr_type_coarse, 'db_arr_type_coarse')
write_file_it(db_arr_type_fine, 'db_arr_type_fine')
write_file(db_arr_q, 'db_arr_q')

# save counts and write to files

db_arr_cat_count = count_it(db_arr_cat)
db_arr_type_count_flat = count_it(db_arr_type2)
db_arr_type_coarse_flat = count_it(db_arr_type_coarse)
db_arr_type_fine_flat = count_it(db_arr_type_fine)

# sort according to number of occurrences
sort_db_arr_type_count = sorted(db_arr_type_count_flat.items(), key=lambda x: x[1], reverse=True)
sort_db_arr_type_count_fine = sorted(db_arr_type_fine_flat.items(), key=lambda x: x[1], reverse=True)
sort_db_arr_type_count_coarse = sorted(db_arr_type_coarse_flat.items(), key=lambda x: x[1], reverse=True)

print('number of distinct types in training data', len(sort_db_arr_type_count))
print('number of distinct types in training data: fine', len(sort_db_arr_type_count_fine))
print('number of distinct types in training data: coarse', len(sort_db_arr_type_count_coarse))

write_file(db_arr_cat_count, 'db_arr_cat_count')
write_file(sort_db_arr_type_count, 'db_arr_type_count2')
write_file(sort_db_arr_type_count_fine, 'sort_db_arr_type_count_fine')
write_file(sort_db_arr_type_count_coarse, 'sort_db_arr_type_count_coarse')
