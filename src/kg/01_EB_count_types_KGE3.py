def read_file(filename, delm):
    noun_list = open('data/' + filename, 'r')
    file = []
    for line in noun_list:
        output_list = line.split(delm)  # delimit on ]
        file.append(output_list)
    noun_list.close()
    return file


def write_file(file_to_write, filename):
    myFile = open('data/' + filename + '.txt', 'w')
    myFile.write(str(file_to_write))
    myFile.write('\n')
    myFile.close()
    return 0


db_noun_types = read_file('db_noun_typ.txt', '}, {')
db_np_types = read_file('db_np_typ.txt', '}, {')

'''count types'''


def count_it(lst):
    # print(lst)
    counts = dict()
    for i in lst:
        for l in i:     # accesses question level types: in another list
            try:
                type = next(iter(l))    # get 'first' type in list
                counts[type] = counts.get(type, 0) + 1
            except Exception as e:
                print(e)
    return counts


type_counts_db_fin = count_it(db_noun_types)
# type_counts_db2_fin = count_it(db_noun_types2)

type_counts_dbnp_fin = count_it(db_np_types)
# type_counts_dbnp2_fin = count_it(db_np_types2)

write_file(type_counts_db_fin, 'type_counts_db_fin')
# write_file(type_counts_db2_fin, 'type_counts_db2_fin')
write_file(type_counts_dbnp_fin, 'type_counts_dbnp_fin')
# write_file(type_counts_dbnp2_fin, 'type_counts_dbnp2_fin')

print('counting types done')
