# create vectors using word embeddings and knowledge graph embeddings
# Eleanor Bill 4 September 2020

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
import pickle
from textblob import TextBlob
from nltk.corpus import stopwords
from kg.endpoints import DBpediaEndpoint
from kg.lookup import DBpediaLookup

stopWords = set(stopwords.words('english'))


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
# dbpedia_train = dbpedia_train[0:5]  # shorten for purposes of testing
# print('done shorten')

# remove none questions - clean data
for entry in dbpedia_train:
    if entry['question'] is None:
        dbpedia_train.remove(entry)


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
for entry in dbpedia_train_wh:
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

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '05_dbpedia_train_wh')
print('done types found')

# pickle
f = open("data/dbpedia_train_wh.pkl","wb")
pickle.dump(dbpedia_train_wh,f)
f.close()

