"""create vectors for test data"""
# 9th sept - ejb

import re
import json
import nltk
import pickle
import requests
import numpy as np
from gensim.models import KeyedVectors
from textblob import TextBlob
from nltk.corpus import stopwords
from kg.endpoints import DBpediaEndpoint
from kg.lookup import DBpediaLookup
from util.utilities import getEntityName

stopWords = set(stopwords.words('english'))


def write_file(file_to_write, filename):
    myFile = open('data/' + filename + '.txt', 'w')
    myFile.write(str(file_to_write))
    myFile.write('\n')
    myFile.close()
    return 0


""" load test data """


def load_json(filename):
    with open(filename + ".json") as json_file:
        data = json.load(json_file)
    json_file.close()
    return data


dbpedia_test = load_json("data/smarttask_dbpedia_test_questions.json")  # to list of dictionaries

# remove none questions - clean data
for entry in dbpedia_test:
    if entry['question'] is None:
        dbpedia_test.remove(entry)


"""PARSING AND EXTRACTION"""


def find_w(question):  # search questions for given wh words
    # in order of how important they are e.g. only use those near end of list if those closer to the front aren't found
    wh_words = ['why', 'where', 'when', 'how', 'which', 'what', 'who', 'whose', 'whom', 'does', 'is it true', 'name a',
                'name the', 'tell me', 'did', 'give', 'is the', 'is', 'was', 'are']
    # lowercase
    wh = []
    for a in wh_words:  # search for each word in above array
        if re.search(a, question.lower()):
            wh.append(a)  # if found, append
    if len(wh) == 0:
        wh.append('N/A')
    return wh


re_list = []
for a in dbpedia_test:
    temp = find_w(a['question'])
    a.update({'wh': str(temp[0])})
    re_list.append(a)

print('done find wh')
dbpedia_test = re_list
write_file(dbpedia_test, '01_dbpedia_test')


# parse and extract nouns
def nouns(question):
    tokens = nltk.word_tokenize(question)
    tags = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    return nouns


re_list = []
for entry in dbpedia_test:
    question = entry['question']
    noun_list = nouns(question)
    entry.update({'noun list': noun_list})
    re_list.append(entry)

dbpedia_test = re_list
write_file(dbpedia_test, '02_dbpedia_test')
print('done nouns parsed')


# parse and extract noun phrases
def noun_phrases(question):
    blob = TextBlob(question)
    noun_phrases = blob.noun_phrases
    np2 = list(noun_phrases)  # convert from wordlist to list
    return np2


re_list = []
for entry in dbpedia_test:
    question = entry['question']
    np_list = noun_phrases(question)
    entry.update({'np list': np_list})
    re_list.append(entry)

dbpedia_test = re_list
write_file(dbpedia_test, '03_dbpedia_test')
print('done noun phrases parsed')


# filter out stopwords and special characters from np lists
def filter_SW(lst):
    wordsFiltered = []
    lst = list(filter(None, lst))  # remove any empty strings
    for w in lst:  # for word in list of nouns
        w = re.sub('\[', ' ', w)
        w = re.sub('[^A-Za-z0-9\' ]+', '', w)
        if w not in stopWords and w != "''":
            wordsFiltered.append(w)
    return wordsFiltered


re_list = []
for entry in dbpedia_test:
    nps = entry['np list']
    np_list = filter_SW(nps)
    entry.update({'np list': np_list})
    re_list.append(entry)

dbpedia_test = re_list
write_file(dbpedia_test, '04_dbpedia_test')
print('done nps filtered')

''' KG lookup to return set of related entities and closest type for each '''
folder_ontos = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/"
uri_onto = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/dbpedia_2014_fix.owl"


def get_entities(phrase):  # question as a list of words
    limit = 1
    if phrase != "''":
        dbpedia = DBpediaLookup()  # look up in DBP KG
        entities = dbpedia.getKGEntities(phrase, limit)
    else:
        entities = ['N/A']
    if len(entities) > 0:
        return entities[0]
    else:
        return ['N/A']


def apply_endpoint(entity):  # find types
    ep = DBpediaEndpoint()  # using ID/int
    ent2 = entity.getIdstr()
    types = ep.getTypesForEntity(ent2)  # limit to 5
    # print('types using endpoint id', types)
    if len(types) == 0:  # using entity: back up
        types = entity.getTypes()  # ont
        # print('types using entity', types, '\n')
    return types


# run noun phrases through KGE to find entity, type
re_list = []
for entry in dbpedia_test:
    np_entities = []
    for n in entry['np list']:
        ent = get_entities(n)
        # print('ent', ent, '\n length', len(ent), len(n))
        np_entities.append(ent)
    entry.update({'entities': np_entities})
    entity_types = []
    for a in entry['entities']:
        if a != ['N/A']:
            types = apply_endpoint(a)  # a single entity in a list
            if len(types) > 0:
                entity_types.append(types)
    entry.update({'entity_types': entity_types})
    re_list.append(entry)

dbpedia_test = re_list
write_file(dbpedia_test, '05_dbpedia_test')
print('done types found')


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
for entry in dbpedia_test:
    # print(entry['wh'])
    we = find_vector_we(entry['wh'])
    # print(we)
    entry.update({'we_wh_vector': we})
    re_list.append(entry)

dbpedia_test = re_list
write_file(dbpedia_test, '06_dbpedia_test')
print('done wh WE vectors found')

# run nouns through word embedding
re_list = []
for entry in dbpedia_test:
    we_nouns = []
    for noun in entry['noun list']:
        we = find_vector_we(noun)
        if len(we) > 0:  # removed zeroed vectors to avoid affecting average
            we_nouns.append(we)
    average_vector = cal_average(we_nouns)
    entry.update({'we_nouns_vector': average_vector})
    re_list.append(entry)

dbpedia_test = re_list
write_file(dbpedia_test, '07_dbpedia_test')
print('done noun WE vectors found')

# run nps through word embedding
re_list = []
for entry in dbpedia_test:
    we_np = []
    for n in entry['np list']:
        we = find_vector_we(n)
        if len(we) > 0:  # removed zeroed vectors to avoid affecting average
            we_np.append(we)
    average_vector = cal_average(we_np)
    entry.update({'we_np_vector': average_vector})
    re_list.append(entry)

dbpedia_test = re_list
write_file(dbpedia_test, '08_dbpedia_test')
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
for entry in dbpedia_test:
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
dbpedia_test = re_list
write_file(dbpedia_test, '10_dbpedia_test')
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
for entry in dbpedia_test:
    kge_entities = []
    for noun_phrase in entry['np list']:
        kge = find_vector_kge(noun_phrase)
        if len(kge) > 1:
            kge_entities.append(kge)
    average_vector = cal_average(kge_entities)
    entry.update({'entities_KGE_vector': average_vector})
    re_list.append(entry)

print('done entities KGE vectors found')
dbpedia_test = re_list
write_file(dbpedia_test, '11_dbpedia_test')


def concatenate_vector(entry):
    cv = [entry['we_wh_vector'],
          entry['we_nouns_vector'],
          entry['we_np_vector'],
          entry['entities_KGE_vector'],
          entry['we_type_vector']]
    return cv


re_list = []
for entry in dbpedia_test:
    concatenated_vector = concatenate_vector(entry)
    entry.update({'concatenated_vector': concatenated_vector})
    re_list.append(entry)

print('done concatenate vector')
dbpedia_test = re_list
write_file(dbpedia_test, '12_dbpedia_test')

# pickle
f = open("data/dbpedia_test_final.pkl","wb")
pickle.dump(dbpedia_test,f)
f.close()