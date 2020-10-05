'''author: Eleanor Bill @eljne'''
''' stores functions that are used at multiple points throughout the program '''

import json
import re
import nltk
import os
from nltk.tokenize import word_tokenize
import pickle
import requests
import numpy as np
from textblob import TextBlob
from kg.endpoints import DBpediaEndpoint
from kg.lookup import DBpediaLookup
from util.utilities import getEntityName

'''loading functions'''


def write_file(file_to_write, filename):
    myFile = open('data/' + filename + '.txt', 'w')
    myFile.write(str(file_to_write))
    myFile.write('\n')
    myFile.close()
    return 0


def read_file(filename):
    myFile = open('data/' + filename + '.txt', 'r')
    load = myFile.read()
    myFile.close()
    return load


# load training data
def load_json(filename):
    with open(filename + ".json") as json_file:
        data = json.load(json_file)
    json_file.close()
    return data


def pickl(filename, object_name):
    f = open("data/" + filename + ".pkl", "wb")
    pickle.dump(object_name,f)
    f.close()
    return 0


def unpickle(filename):
    pkl_file = open('data/' + filename + '.pkl', 'rb')
    return_file = pickle.load(pkl_file)
    pkl_file.close()
    return return_file


def try_to_load_as_pickled_object_or_None(filepath):
    """
    This is a defensive way to write pickle.load, allowing for very large files on all platforms
    """
    max_bytes = 2**31 - 1
    try:
        input_size = os.path.getsize(filepath)
        bytes_in = bytearray(0)
        with open(filepath, 'rb') as f_in:
            for _ in range(0, input_size, max_bytes):
                bytes_in += f_in.read(max_bytes)
        obj = pickle.loads(bytes_in)
    except:
        return None
    return obj


'''PARSING AND EXTRACTION FUNCTIONS'''


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


# parse and extract nouns using NLTK
def nouns(question):
    tokens = nltk.word_tokenize(question)
    tags = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    return nouns


# parse and extract nouns using NLTK
def nouns_list(lst):
    ns = []
    for l in lst:
        tokens = nltk.word_tokenize(l)
        tags = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
        ns.append(nouns)
    return ns


# parse and extract noun phrases using TextBlob
def noun_phrases(question):
    blob = TextBlob(question)
    noun_phrases = blob.noun_phrases
    np2 = list(noun_phrases)  # convert from wordlist to list
    return np2


# parse and extract noun phrases using TextBlob
def noun_phrases_list(lst):
    nps = []
    for l in lst:
        blob = TextBlob(l)
        noun_phrases = blob.noun_phrases
        np2 = list(noun_phrases)  # convert from wordlist to list
        nps.append(np2)
    return nps


# filter out stopwords and special characters from np lists
def filter_SW(lst, stopWords):
    wordsFiltered = []
    lst = list(filter(None, lst))  # remove any empty strings
    for item in lst:  # for word in list of nouns
        phrase = []
        arr = word_tokenize(item)
        for w in arr:
            w = re.sub('\[', ' ', w)
            w = re.sub('[^A-Za-z0-9\' ]+', '', w)
            if w not in stopWords and w != "''":
                phrase.append(w)
        wordsFiltered.append(phrase)
    return wordsFiltered


''' KG lookup to return set of related entities and closest type for each '''


def get_entities(phrase):  # question as a list of words
    limit = 1
    if phrase != "''":
        dbpedia = DBpediaLookup()  # look up in DBP KG
        entities = dbpedia.getKGEntities(phrase, limit)
    else:
        entities = ['N/A']
    if len(entities) > 0:
        return entities[0]  # return only first entity
    else:
        return ['N/A']  # if no entities, return 'n/a'


def get_entities_list(np_list):  # question as a list of words
    entity_list = []
    for phrase in np_list:
        limit = 1
        if phrase != "''":
            dbpedia = DBpediaLookup()  # look up in DBP KG
            entities = dbpedia.getKGEntities(phrase, limit)
        else:
            entities = ['N/A']
        if len(entities) > 0:
            entity_list.append(entities[0]) # append only first entity
        else:
            entity_list.append(['N/A'])  # if no entities, return 'n/a'
    return entity_list


def apply_endpoint(entity):  # find types
    # print(entity)
    ep = DBpediaEndpoint()  # using ID/int
    ent2 = entity.getIdstr()
    types = ep.getTypesForEntity(ent2)  # limit to 5
    # print('types using endpoint id', types)
    if len(types) == 0:  # using entity: back up
        types = entity.getTypes()  # ont
        # print('types using entity', types, '\n')
    return types


def apply_endpoint_list(entity_list):  # find types
    types_list = []
    ep = DBpediaEndpoint()  # using ID/int
    for entity in entity_list:
        print(entity)
        # ['N/A']
        # < id: http://dbpedia.org/resource/Ana_Popović, label: Ana Popović, description: None, types: set(), source: DBpedia >
        if entity != ['N/A']:
            ent2 = entity.getIdstr()
            types = ep.getTypesForEntity(ent2)  # limit to 5
            # print('types using endpoint id', types)
            types_list.append(types)
            if len(types) == 0:  # using entity: back up
                types = entity.getTypes()  # ont
                # print('types using entity', types, '\n')
                types_list.append(types)
        else:
            types = []
            types_list.append(types)
    return types_list



''' creating the vectors '''


# find word embedding vector
def find_vector_we(word_or_phrase, loaded_model):
    try:
        vector = loaded_model.word_vec(word_or_phrase)
    except:
        vector = np.zeros(1)
    return vector


# find average of vectors
def cal_average(question_vector):
    avg = np.average(question_vector, axis=0)
    return avg


#   get the entity name for a given URI
def type_convert(ty):
    label = getEntityName(ty)
    return label


#   find KG embedding vector using REST API
#   if not found, return zeroed vector of same length
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


# get last dbpedia entity
def get_last(ls):
    count = -1
    try:
        el = list(ls)
        ret = str(el[count])
        while "dbpedia" not in ret:
            count = count - 1
            ret = str(el[count])
        return ret
    except:
        return None

def get_last_2(ls):
    count = -1
    try:
        el = list(ls)
        ret = str(el[count])
        return ret
    except:
        return None


def reformat(row_column):
    row_concatv = row_column['concatenated_vector']
    flat_array = [item for sublist in row_concatv for item in sublist]
    return flat_array

'''Also for boolean, numerical or date questions, the key may be in the type of questions or Wh questions. 
We can train a specific classifier for them, or apply heuristics (or both).  e.g. Is x greater than y? 
When x happened? Does x is y? Ho many...? Seem to have a clear type with independence of the content.
    '''


# apply before getting top ten / top category/type
def replace_Location(l):
    new_l = []
    for item in l:
        if item[0] == 'dbo:Location':
            item2 = ('dbo:Place', item[1])
        else:
            new_l.append(item)
    return new_l


def replace_Location_2(l):
    new_l = []
    for item in l:
        if item == 'dbo:Location':
            new_l.append('dbo:Place')
        else:
            new_l.append(item)
    return new_l


def heuristics(dct, wh, lb):
    if lb == 'type':
        if wh in ('does', 'is it true', 'did', 'is the', 'is', 'was', 'are'):
            dct["boolean"] = 1.00
        if wh == 'when':
            dct["date"] = 1.00
            dct["boolean"] = 0.00
        if wh == 'where':
            dct['dbo:Place'] = 1.00
            dct["boolean"] = 0.00
        if wh in ('who', 'whose', 'whom'):
            dct['dbo:Person'] = 1.00
            dct["boolean"] = 0.00
    if lb == 'category':
        if wh in ('does', 'is it true', 'did', 'is the', 'is', 'was', 'are'):
            dct["boolean"] = 1.00
        if wh == 'when':
            dct["literal"] = 1.00
            dct["boolean"] = 0.00
        if wh == 'where':
            dct["boolean"] = 0.00
        if wh in ('who', 'whose', 'whom'):
            dct["boolean"] = 0.00
        if wh in ('why', 'how', 'which', 'what', 'name a', 'name the', 'tell me', 'give'):
            dct["boolean"] = 0.00
    return dct


def heuristics_2(row):
    new_row = row.copy()
    if row['category'] == 'boolean':
        new_row['type'] = 'boolean'    # If the category is "boolean" the answer type is always "boolean".
    if row['category'] == 'literal':    # If the category is "literal", answer types are either "number", "date",
        # "string" or "boolean" answer type.
        new_types_list = [] # prioritize more likely
        for a in row['type']:
            if a in ('number', 'date', 'string', 'boolean'):
                new_types_list.append(a)
        for a in row['type']:
            if a not in ('number', 'date', 'string', 'boolean'):
                new_types_list.append(a)
        new_row['type'] = new_types_list[0:10]
    return new_row
