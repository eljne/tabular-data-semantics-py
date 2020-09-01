# create vectors using word embeddings and knowledge graph embeddings
# Eleanor Bill 26 August 2020

'''
list of created vectors/steps:
    wh - word embedding
    noun list - word embedding
    noun phrase list - word embedding
    noun phrase list - lookup to get related entities
    related entities - KG embedding
    most specific type - WE if any

'''

import re
import json
import nltk
import pandas as pd
import requests
import numpy as np
from textblob import TextBlob
from nltk.corpus import stopwords
from collections import defaultdict

stopWords = set(stopwords.words('english'))  # load stopwords
from ontology.onto_access import OntologyAccess, DBpediaOntology, SchemaOrgOntology
from kg.endpoints import SPARQLEndpoint, DBpediaEndpoint
from kg.lookup import Lookup, DBpediaLookup, WikidataAPI


def write_file(file_to_write, filename):
    myFile = open('data/' + filename + '.txt', 'w')
    myFile.write(str(file_to_write))
    myFile.write('\n')
    myFile.close()
    return 0


# load training data
def load_json(filename):
    with open(filename + ".json") as json_file:
        data = json.load(json_file)
    json_file.close()
    return data


dbpedia_train = load_json("data/smarttask_dbpedia_train")  # to list of dictionaries
dbpedia_train = dbpedia_train[0:5]  # shorten for purposes of testing
print('done shorten')

'''PARSING AND EXTRACTION'''


# search questions for given wh words
def find_w(question):
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
for a in dbpedia_train:
    temp = find_w(a['question'])
    a.update({'wh': str(temp[0])})
    re_list.append(a)

print('done find wh')
dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '01_dbpedia_train_wh')

''' rules for wh '''
'''
answer categories: resource, literal or boolean

if wh is 'is', 'does', 'is it true', 'did', 'is the', 'are': boolean x

answer types: involve ontology/word embedding

if wh is 'how many' = number x
if wh is 'when' = date x
if category is boolean = boolean x

if category is resource - ontology
if category is literal - "number", "date", "string", "boolean"

['why', 'where', 'when', 'how', 'which', 'what', 'who', 'whose', 'whom', 'does', 'is it true', 'name a',
                'name the', 'tell me', 'did', 'give', 'is the', 'is', 'was', 'are']

'''

for question in dbpedia_train_wh:
    if question['wh'] in ('is', 'does', 'is it true', 'did', 'is the', 'are'):
        question.update({'found category': 'ho'})
    elif question['wh'] in ('how many', 'when'):
        question.update({'found category': 'literal'})
    elif question['wh'] in ('who'):
        question.update({'found category': 'resource'})
    else:
        question.update({'found category': 'unknown'})

print('done quick answer cat rules')

for question in dbpedia_train_wh:
    if question['found category'] in ('boolean'):
        question.update({'found type': 'boolean'})
    elif question['wh'] in ('how many'):
        question.update({'found type': 'number'})
    elif question['wh'] in ('when'):
        question.update({'found type': 'date'})
    else:
        question.update({'found type': 'unknown'})

print('done quick answer type rules')


# parse and extract nouns
def nouns(question):
    tokens = nltk.word_tokenize(question)
    tags = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    return nouns


re_list = []
for entry in dbpedia_train_wh:
    question = entry['question']
    noun_list = nouns(question)
    entry.update({'noun list': noun_list})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '02_dbpedia_train_wh')
print('done nouns parsed')


# parse and extract noun phrases
def noun_phrases(question):
    blob = TextBlob(question)
    noun_phrases = blob.noun_phrases
    np2 = list(noun_phrases)  # convert from wordlist to list
    return np2


re_list = []
for entry in dbpedia_train_wh:
    question = entry['question']
    np_list = noun_phrases(question)
    entry.update({'np list': np_list})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '03_dbpedia_train_wh')
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
for entry in dbpedia_train_wh:
    nps = entry['np list']
    np_list = filter_SW(nps)
    entry.update({'np list': np_list})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '04_dbpedia_train_wh')
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
        entities = []
    for et in entities:  # return just one entity, outside a list format
        e = et
    return e


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
for entry in dbpedia_train_wh:
    np_entities = []
    for n in entry['np list']:
        ent = get_entities(n)
        # print('ent', ent, '\n length', len(ent), len(n))
        np_entities.append(ent)
    entry.update({'entities': np_entities})
    entity_types = []
    for a in entry['entities']:
        # print('a', a)
        types = apply_endpoint(a)  # a single entity in a list
        if len(types) > 0:
            entity_types.append(types)
    entry.update({'entity_types': entity_types})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '05_dbpedia_train_wh')
print('done types found')

''' word embeddings on wh and nouns '''

from gensim.models import KeyedVectors

fastTextfile = 'data/wiki-news-300d-1M.vec'
loaded_model = KeyedVectors.load_word2vec_format(fastTextfile)


# find word embedding vector
def find_vector_we(word_or_phrase):
    try:
        vector = loaded_model.wv.word_vec(word_or_phrase)
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
    print(entry['wh'])
    we = find_vector_we(entry['wh'])
    print(we)
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

# run related entities through word embedding
re_list = []
for entry in dbpedia_train_wh:
    we_entities = []
    for ent in entry['entities']:
        we = find_vector_we(ent)
        if len(we) > 0:  # removed zeroed vectors to avoid affecting average
            we_entities.append(we)
    average_vector = cal_average(we_entities)
    entry.update({'we_entities_vector': average_vector})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '09_dbpedia_train_wh')
print('done entity WE vectors found')

# run closest type through word embedding
re_list = []
for entry in dbpedia_train_wh:
    we_type = []
    for type in entry['entity_types']:
        we = find_vector_we(type)
        if len(we) > 0:  # removed zeroed vectors to avoid affecting average
            we_type.append(we)
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


# run entities through kg embedding to get vectors
re_list = []
for entry in dbpedia_train_wh:
    kge_entities = []
    for noun_phrase in entry['entities']:
        kge = find_vector_kge(noun_phrase)
        if len(we) > 1:
            kge_entities.append(kge)
    average_vector = cal_average(kge_entities)
    entry.update({'entities_KGE_vector': average_vector})
    re_list.append(entry)

print('done entities KGE vectors found')
dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '11_dbpedia_train_wh')

'''
we_wh_vector - First position could be for the embedding of the wh question word (we can create our own embedding/encoding).
we_nouns_vector - Second position for the WE of the sentence or set of nouns.
we_np_vector - Third position (up to 3 or 4 vector positions? we can play with different values) for noun phrases without a good correspondence in KG (WE of the noun phrase)
entities_KGE_vector - Fourth position (up to 3 or 4 vector positions) for noun phrases with a good correspondence in KG (KGE of entity representing noun phrase)
we_type_vector - Fifth position (up to 3 or 4 vector positions) for the WE of the types of the KG entities above.
'''


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

# convert to dataframe to split
df_all = pd.DataFrame()

df = pd.DataFrame(dbpedia_train_wh)
print(df.head(4))

print('done convert to df')

# group by on categories, types


# vectors created to use with classifiers
# group vector by categories, types

# find unique categories, types

categories_list = ['boolean', 'literal', 'resource']
temp = []
for entry in dbpedia_train_wh:
    ty = entry['type']
    temp.append(ty)
types_list = np.unique(temp)

print('done found uniques')

dict_of_types = dict(iter(df.groupby('type')))
dict_of_categories = dict(iter(df.groupby('category')))

print('done split to types and categories')
