# input: list of class/type frequency: type_counts_

# sample_lookup in SemAIDA

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

'''

Read existing entities and classes

'''

db_entities = read_file('')
db_np_entities = read_file('')


'''

Read existing questions

'''

db_questions = read_file('')

'''

lookup new entities and classes

'''




'''

update entities and classes to files 

'''

write_file(, 'sample_gen')
