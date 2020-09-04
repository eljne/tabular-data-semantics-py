# Eleanor Bill 4 September 2020
# continue creating vectors

import requests
import numpy as np
from gensim.models import KeyedVectors
from util.utilities import getEntityName
import pickle
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))  # load stopwords

pkl_file = open('data/dbpedia_train_wh.pkl', 'rb')
dbpedia_train_wh = pickle.load(pkl_file)
pkl_file.close()


def write_file(file_to_write, filename):
    myFile = open('data/' + filename + '.txt', 'w')
    myFile.write(str(file_to_write))
    myFile.write('\n')
    myFile.close()
    return 0


''' word embeddings on wh and nouns '''
fastTextfile = 'data/wiki-news-300d-1M.vec'
loaded_model = KeyedVectors.load_word2vec_format(fastTextfile)


# find word embedding vector
def find_vector_we(word_or_phrase):
    try:
        vector = loaded_model.word_vec(word_or_phrase)
    except:
        vector = np.zeros(1)
    return vector


# find average of vectors
def cal_average(question_vector):
    avg = np.average(question_vector, axis=0)
    return avg


# run wh through word embedding
re_list = []
for entry in dbpedia_train_wh:
    # print(entry['wh'])
    we = find_vector_we(entry['wh'])
    # print(we)
    entry.update({'we_wh_vector': we})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '06_dbpedia_train_wh')
print('done wh WE vectors found')

# run nouns through word embedding
re_list = []
for entry in dbpedia_train_wh:
    we_nouns = []
    for noun in entry['noun list']:
        we = find_vector_we(noun)
        if len(we) > 0:  # removed zeroed vectors to avoid affecting average
            we_nouns.append(we)
    average_vector = cal_average(we_nouns)
    entry.update({'we_nouns_vector': average_vector})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '07_dbpedia_train_wh')
print('done noun WE vectors found')

# run nps through word embedding
re_list = []
for entry in dbpedia_train_wh:
    we_np = []
    for n in entry['np list']:
        we = find_vector_we(n)
        if len(we) > 0:  # removed zeroed vectors to avoid affecting average
            we_np.append(we)
    average_vector = cal_average(we_np)
    entry.update({'we_np_vector': average_vector})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '08_dbpedia_train_wh')
print('done noun phrase WE vectors found')


#   get the entity name for a given URI
def type_convert(ty):
    label = getEntityName(ty)
    return label

#   query the SPARQL endpoint to get the label
# def type_convert(ty):
#     ep = SPARQLEndpoint(ty)
#     label = ep.getEnglishLabelsForEntity(ty)
#     return label


# run closest type through word embedding
re_list = []
for entry in dbpedia_train_wh:
    we_type = []
    for t in entry['entity_types']:
        ty = next(iter(t))
        english_label = type_convert(ty)
        we2 = find_vector_we(english_label)
        if len(we2) > 0:  # removed zeroed vectors to avoid affecting average
            we_type.append(we2)
    average_vector = cal_average(we_type)
    entry.update({'we_type_vector': average_vector})
    re_list.append(entry)

del loaded_model  # delete WE model from memory
dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '10_dbpedia_train_wh')
print('done type WE vectors found')

''' use kgvec2go KGEs '''
''' link to kg embeddings using nouns and nps to find types '''
'''# Use pre-trained kg embeddings and concatenate or average them to create the vector for the question.'''


def find_vector_kge(word_or_phrase):
    try:
        word_or_phrase = word_or_phrase.replace(" ", "_")
        query = 'http://www.kgvec2go.org/rest/get-vector/dbpedia/' + str(word_or_phrase)
        response = requests.get(query)
        r2 = response.json()
        vector = r2['vector']
    except:
        try:
            word_or_phrase1 = word_or_phrase.replace("_", " ")
            word_or_phrase = word_or_phrase1.title()  # capitalise each first letter to catch e.g. names
            word_or_phrase2 = word_or_phrase.replace(" ", "_")  # replace w/underscores again for API
            query = 'http://www.kgvec2go.org/rest/get-vector/dbpedia/' + str(word_or_phrase2)
            response = requests.get(query)
            r2 = response.json()
            vector = r2['vector']
        except:
            vector = np.zeros(1)
    return vector


# run noun phrases through kg embedding to get vectors
re_list = []
for entry in dbpedia_train_wh:
    kge_entities = []
    for noun_phrase in entry['np list']:
        kge = find_vector_kge(noun_phrase)
        if len(kge) > 1:
            kge_entities.append(kge)
    average_vector = cal_average(kge_entities)
    entry.update({'entities_KGE_vector': average_vector})
    re_list.append(entry)

print('done entities KGE vectors found')
dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '11_dbpedia_train_wh')

f = open("data/dbpedia_train_all_vectors.pkl","wb")
pickle.dump(dbpedia_train_wh,f)
f.close()

print('ALL done pickled')