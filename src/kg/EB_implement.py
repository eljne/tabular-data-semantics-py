'''
Created on 19 Mar 2019
@author: ejimenez-ruiz

Edited on 5th August 2020
@author: eljne

'''

import re
from ontology.onto_access import OntologyAccess, DBpediaOntology, SchemaOrgOntology
import re
from kg.endpoints import SPARQLEndpoint, DBpediaEndpoint
from kg.lookup import Lookup, DBpediaLookup, WikidataAPI
import itertools
from nltk.corpus import stopwords

'''
load ontologies
'''

folder_ontos = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/"

# locations for different ontologies (owl files)
# uri_onto = "http://www.cs.ox.ac.uk/isg/ontologies/dbpedia.owl"
# uri_onto = "http://www.cs.ox.ac.uk/isg/ontologies/schema.org.owl"
# uri_onto="/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/dbpedia.owl"
uri_onto = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/dbpedia_2014_fix.owl"
# uri_onto="/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/schema.org.owl"

# onto_access = OntologyAccess(uri_onto)
# onto_access = DBpediaOntology()
onto_access = SchemaOrgOntology()

onto_access.loadOntology(True)

'''
load parsed questions
'''


# noun lists

def read_file(filename, delm):
    noun_list = open('data/' + filename, 'r')
    file = []
    for line in noun_list:
        output_list = line.split(delm)  # delimit on ]
        file.append(output_list)
    noun_list.close()
    return file


db_noun_list = read_file('db_noun_list.txt', '],')
wd_noun_list = read_file('wd_noun_list.txt', '],')
db_noun_phrase_list = read_file('db_nounphrase_list.txt', '],')
wd_noun_phrase_list = read_file('wd_nounphrase_list.txt', '],')

print('done')


# filter out stopwords and special characters from lists
def filter_SW(lst, splitter):
    wordsFiltered = []
    for line in lst:
        ws = line.split(splitter)
        ws = list(filter(None, ws))
        for w in ws:
            w = re.sub('\[', ' ', w)
            w = re.sub('[^A-Za-z0-9\' ]+', '', w)
            if w not in stopWords and w != "''":
                wordsFiltered.append(w)
    return wordsFiltered


# shorten just for testing
# db_noun_list = db_noun_list[0:5]
# wd_noun_list = wd_noun_list[0:5]
# db_noun_phrase_list = db_noun_phrase_list[0:5]
# wd_noun_phrase_list = wd_noun_phrase_list[0:5]

stopWords = set(stopwords.words('english'))  # load stopwords

db_noun_list_flt = []
wd_noun_list_flt = []
db_noun_phrase_list_flt = []
wd_noun_phrase_list_flt = []

for q in db_noun_list:
    temp = filter_SW(q, ' ')
    db_noun_list_flt.append(temp)

for q in wd_noun_list:
    temp = filter_SW(q, ' ')
    wd_noun_list_flt.append(temp)

for q in db_noun_phrase_list:
    temp = filter_SW(q, ',')
    db_noun_phrase_list_flt.append(temp)

for q in wd_noun_phrase_list:
    temp = filter_SW(q, ',')
    wd_noun_phrase_list_flt.append(temp)

print('done')

print(db_noun_list_flt)
print(wd_noun_list_flt)
print(db_noun_phrase_list_flt)
print(wd_noun_phrase_list_flt)


'''
get entities for all using lookup
'''

db_noun_ent = []
wd_noun_ent = []
db_np_ent = []
wd_np_ent = []


def get_entities(q_lst):  # question as a list of words
    question_entities = []
    types_lkup = []
    limit = 1
    for w in q_lst:
        if w != "''":
            dbpedia = DBpediaLookup()   # look up in DBP KG
            entities = dbpedia.getKGEntities(w, limit)
            for ent in entities:
                # print(w, 'DBPedia', ent)
                question_entities.append(ent)
    return question_entities


for a in db_noun_list_flt:
    question_entities = get_entities(a)
    db_noun_ent.append(question_entities)

for a in wd_noun_list_flt:
    question_entities = get_entities(a)
    wd_noun_ent.append(question_entities)

for a in db_noun_phrase_list_flt:
    question_entities = get_entities(a)
    db_np_ent.append(question_entities)

for a in wd_noun_phrase_list_flt:
    question_entities = get_entities(a)
    wd_np_ent.append(question_entities)

print('done')

print(db_noun_ent)
print(wd_noun_ent)
print(db_np_ent)
print(wd_np_ent)

'''
get types for all using endpoint
'''

# shorten array for test
db_noun_ent = db_noun_ent[0:2]
wd_noun_ent = wd_noun_ent[0:2]
db_np_ent = db_np_ent[0:2]
wd_np_ent = wd_np_ent[0:2]


def apply_endpoint(entity_list):  # question level
    types_list = []
    types_list_2 = []

    for ent in entity_list:
        ep = DBpediaEndpoint()

        # finding types

        # using ID/int
        ent2 = ent.getIdstr()
        types = ep.getTypesForEntity(ent2)
        types_list.append(types)
        print('all types for entity using endpoint id', len(types), types, '\n')

        # using entity
        types2 = ent.getTypes()  # ont
        types_list_2.append(types2)
        print('all types using entity', types2)

    return types_list, types_list_2


db_noun_types, db_noun_types2 = apply_endpoint(db_noun_ent)
wd_noun_types, wd_noun_types2 = apply_endpoint(wd_noun_ent)
db_np_types, db_np_types2 = apply_endpoint(db_np_ent)
wd_np_types, wd_np_types2 = apply_endpoint(wd_np_ent)

print(db_noun_types, db_noun_types2)

print('done')

'''
get classes using ontology.onto_access  
'''

db_noun_cls = []
wd_noun_cls = []
db_np_cls = []
wd_np_cls = []


def apply_onto_access(q_lst):
    onto_access_list = []
    for w in q_lst:
        if w != "''":
            onto_access = OntologyAccess()   # look up in DBP KG
            classes = onto_access.getClassIRIsContainingName(w)
            for cls in classes:
                print(w, 'contained by: ', cls)
                onto_access_list.append(cls)
    return onto_access_list


for a in db_noun_list_flt:
    class_list = apply_onto_access(a)
    db_noun_cls.append(class_list)

for a in wd_noun_list_flt:
    class_list = apply_onto_access(a)
    wd_noun_cls.append(class_list)

for a in db_noun_phrase_list_flt:
    class_list = apply_onto_access(a)
    db_np_cls.append(class_list)

for a in wd_noun_phrase_list_flt:
    class_list = apply_onto_access(a)
    wd_np_cls.append(class_list)

print('done')

print(db_noun_cls)
print(wd_noun_cls)
print(db_np_cls)
print(wd_np_cls)


