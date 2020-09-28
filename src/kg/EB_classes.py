'''author: Eleanor Bill @eljne'''
''' stores functions that are used at multiple points throughout the program '''

import json
import re
import nltk
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



#
# def check_lengths(row, column, length):
#     if len(row[column]) == length:
#         return row[column]
#     else:
#         return np.zeros(length)
#
#
# # make sure all the same length (if returned zeros, replace with array of zeroes that is correct length)
# all_td['we_wh_vector_2'] = all_td.apply(lambda row: check_lengths(row, 'we_wh_vector', 300), axis=1)
# all_td['we_nouns_vector_2'] = all_td.apply(lambda row: check_lengths(row, 'we_nouns_vector', 300), axis=1)
# all_td['we_np_vector_2'] = all_td.apply(lambda row: check_lengths(row, 'we_np_vector', 300), axis=1)
# all_td['entities_KGE_vector_2'] = all_td.apply(lambda row: check_lengths(row, 'entities_KGE_vector', 200), axis=1)
# all_td['we_type_vector_2'] = all_td.apply(lambda row: check_lengths(row, 'we_type_vector', 300), axis=1)
