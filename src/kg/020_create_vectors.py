''' author: Eleanor Bill @eljne '''
'''create vectors from training data using word embeddings and knowledge graph embeddings '''
'''PART 1: parses parts of the question for embedding and finds entities using SPARQL endpoint'''
'''takes 4ish hours to run'''

'''
list of created vectors/steps:
    wh - word embedding
    noun list - word embedding
    noun phrase list - lookup to get related entities
    related entities - KG embedding
    most specific type - WE if any

'''

from nltk.corpus import stopwords
from kg.EB_classes import load_json, pickl
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
pickl('training_vectors/01_dbpedia_train_wh', dbpedia_train_wh)

re_list = []
for entry in dbpedia_train_wh:
    question = entry['question']
    noun_list = nouns(question)
    entry.update({'noun list': noun_list})
    re_list.append(entry)

dbpedia_train_wh = re_list
pickl('training_vectors/02_dbpedia_train_wh', dbpedia_train_wh)
print('done nouns parsed')

re_list = []
for entry in dbpedia_train_wh:
    question = entry['question']
    np_list = noun_phrases(question)
    entry.update({'np list': np_list})
    re_list.append(entry)

dbpedia_train_wh = re_list
pickl('training_vectors/03_dbpedia_train_wh', dbpedia_train_wh)
print('done noun phrases parsed')

re_list = []
for entry in dbpedia_train_wh:
    nps = entry['np list']
    np_list = filter_SW(nps, stopWords)
    entry.update({'np list': np_list})
    re_list.append(entry)

dbpedia_train_wh = re_list
pickl('training_vectors/04_dbpedia_train_wh', dbpedia_train_wh)
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
pickl('training_vectors/05_dbpedia_train_wh', dbpedia_train_wh)
print('done types found')


