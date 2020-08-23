# lexical matching method that uses word embeddings
# Eleanor Bill 20th August 2020

import re
import json
import nltk
from textblob import TextBlob

'''load training data'''


def load_json(filename):
    with open(filename + ".json") as json_file:
        data = json.load(json_file)
    json_file.close()
    return data


# to list of dictionaries
dbpedia_train = load_json("data/smarttask_dbpedia_train")

# shorten for purposes of testing
dbpedia_train = dbpedia_train[0:5]

print('done shorten')

'''parse and extract wh'''


# search questions for given words
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

# difference between resource and literal?


'''parse and extract nouns'''


def nouns(question):
    noun_list = []
    tokens = nltk.word_tokenize(question)
    tags = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    noun_list.append(nouns)
    return noun_list


re_list = []
for question in dbpedia_train_wh:
    noun_list = nouns(question)
    question.update({'noun list': noun_list})
    re_list.append(question)

dbpedia_train_wh = re_list

print('done nouns parsed')

''' parse and extract nps'''


def noun_phrases(question):
    np_list = []
    blob = TextBlob(question)
    np = blob.noun_phrases
    np2 = list(np)  # convert from wordlist to list
    np_list.append(np2)
    return np_list

re_list = []
for question in dbpedia_train_wh:
    np_list = noun_phrases(question)
    question.update({'np list': np_list})
    re_list.append(question)

dbpedia_train_wh = re_list

print('done noun phrases parsed')



''' link to KG embeddings using nouns and nps to find types '''


def find_type_kge(word_or_phrase):

    return type


# run nouns through word embedding to get types
re_list = []
for question in dbpedia_train_wh:
    kge_nouns = []
    for n in question['noun list']:
        kge = find_type_kge(n)
        kge_nouns.append(kge)
    question.update({'kge_nouns_type': kge_nouns})
    re_list.append(question)

print('done noun types found')


# run noun phrases through word embedding to get
re_list = []
for question in dbpedia_train_wh:
    kge_np = []
    for np in question['np list']:
        kge = find_type_kge(np)
        kge_np.append(kge)
    question.update({'kge_np_type': kge_np})
    re_list.append(question)

print('done noun phrase types found')

# delete WE model from memory
del loaded_model



''' use found types and relevant entities to create vector'''



# all info in list of dictionaries
'''
id
question
category
type
wh
noun
np
kge_noun_vector
kge_np_vector
found_category
found_type
'''

# evaluate found types and categories vs. given
