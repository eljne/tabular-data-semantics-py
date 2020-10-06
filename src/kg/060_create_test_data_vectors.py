''' author: Eleanor Bill @eljne '''
''' create vectors for test data '''

from gensim.models import KeyedVectors
from nltk.corpus import stopwords
import json
import numpy as np
from kg.EB_classes import find_w, nouns, noun_phrases, filter_SW
from kg.EB_classes import get_entities, apply_endpoint, cal_average
from kg.EB_classes import type_convert, find_vector_kge, pickl

stopWords = set(stopwords.words('english'))

with open('data/smarttask_dbpedia_test_questions.json') as fp:
    dbpedia_test = json.load(fp)
fp.close()

# remove none questions - clean data
for entry in dbpedia_test:
    if entry['question'] is None:
        dbpedia_test.remove(entry)

"""PARSING AND EXTRACTION"""

re_list = []
for a in dbpedia_test:
    temp = find_w(a['question'])
    a.update({'wh': str(temp[0])})
    re_list.append(a)

print('done find wh')
dbpedia_test = re_list
pickl('testing_vectors/01_dbpedia_test', dbpedia_test)

re_list = []
for entry in dbpedia_test:
    question = entry['question']
    noun_list = nouns(question)
    entry.update({'noun list': noun_list})
    re_list.append(entry)

dbpedia_test = re_list
pickl('testing_vectors/02_dbpedia_test', dbpedia_test)
print('done nouns parsed')

re_list = []
for entry in dbpedia_test:
    question = entry['question']
    np_list = noun_phrases(question)
    entry.update({'np list': np_list})
    re_list.append(entry)

dbpedia_test = re_list
pickl('testing_vectors/03_dbpedia_test', dbpedia_test)
print('done noun phrases parsed')

re_list = []
for entry in dbpedia_test:
    nps = entry['np list']
    np_list = filter_SW(nps, stopWords)
    entry.update({'np list': np_list})
    re_list.append(entry)

dbpedia_test = re_list
pickl('testing_vectors/04_dbpedia_test', dbpedia_test)
print('done nps filtered')

''' KG lookup to return set of related entities and closest type for each '''
folder_ontos = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/"
uri_onto = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/dbpedia_2014_fix.owl"

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
pickl('testing_vectors/05_dbpedia_test', dbpedia_test)
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
    print('.')
    return vector


# run wh through word embedding
re_list = []
for entry in dbpedia_test:
    # print(entry['wh'])
    we = find_vector_we(entry['wh'])
    # print(we)
    entry.update({'we_wh_vector': we})
    re_list.append(entry)

dbpedia_test = re_list
pickl('testing_vectors/06_dbpedia_test', dbpedia_test)
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
pickl('testing_vectors/07_dbpedia_test', dbpedia_test)
print('done noun WE vectors found')

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
pickl('testing_vectors/08_dbpedia_test', dbpedia_test)
print('done type WE vectors found')

''' use kgvec2go KGEs '''
''' link to kg embeddings using nouns and nps to find types '''
''' Use pre-trained kg embeddings and concatenate or average them to create the vector for the question.'''

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

dbpedia_test = re_list
pickl('testing_vectors/09_dbpedia_test', dbpedia_test)
print('done entities KGE vectors found')

