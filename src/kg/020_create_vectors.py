''' author: Eleanor Bill @eljne '''
'''create vectors using word embeddings and knowledge graph embeddings '''
'''takes 5ish hours to run'''

'''
list of created vectors/steps:
    wh - word embedding
    noun list - word embedding
    noun phrase list - word embedding
    noun phrase list - lookup to get related entities
    related entities - KG embedding
    most specific type - WE if any

'''

from nltk.corpus import stopwords
from kg.EB_classes import write_file, load_json, pickl
from kg.EB_classes import find_w, nouns, noun_phrases, filter_SW, get_entities, apply_endpoint

stopWords = set(stopwords.words('english'))
dbpedia_train = load_json("data/smarttask_dbpedia_train")  # load training data to list of dictionaries

# remove empty questions - clean data
for entry in dbpedia_train:
    if entry['question'] is None:
        dbpedia_train.remove(entry)


'''PARSING AND EXTRACTION'''

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

re_list = []
for entry in dbpedia_train_wh:
    question = entry['question']
    noun_list = nouns(question)
    entry.update({'noun list': noun_list})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '02_dbpedia_train_wh')
print('done nouns parsed')

re_list = []
for entry in dbpedia_train_wh:
    question = entry['question']
    np_list = noun_phrases(question)
    entry.update({'np list': np_list})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '03_dbpedia_train_wh')
print('done noun phrases parsed')

re_list = []
for entry in dbpedia_train_wh:
    nps = entry['np list']
    np_list = filter_SW(nps, stopWords)
    entry.update({'np list': np_list})
    re_list.append(entry)

dbpedia_train_wh = re_list
write_file(dbpedia_train_wh, '04_dbpedia_train_wh')
print('done nps filtered')

''' KG lookup to return set of related entities and closest type for each '''
folder_ontos = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/"
uri_onto = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/dbpedia_2014_fix.owl"

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
pickl('dbpedia_train_wh', dbpedia_train_wh)
print('done pickled')


