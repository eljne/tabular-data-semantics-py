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

read classes and types
Step #1: Read candidate classes and their particular entities

'''

class_ent_n = read_file()
class_ent_np = read_file()


'''

Step #2: Query general entities

'''



'''

output general samples

'''

write_file(,'samples_gen')