

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
