'''
Created on 19 Mar 2019
@author: ejimenez-ruiz

Edited on 05 Aug 2020
@author: eljne

'''
from ontology.onto_access import OntologyAccess, DBpediaOntology, SchemaOrgOntology

'''
lookup to find entity
'''
import re
from kg.endpoints import SPARQLEndpoint, DBpediaEndpoint
from kg.lookup import Lookup, DBpediaLookup, WikidataAPI


# load ontologies

folder_ontos = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/"

# locations for different ontologies (owl files)
# uri_onto = "http://www.cs.ox.ac.uk/isg/ontologies/dbpedia.owl"
# uri_onto = "http://www.cs.ox.ac.uk/isg/ontologies/schema.org.owl"
# uri_onto="/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/dbpedia.owl"
uri_onto = "/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/dbpedia_2014_fix.owl"
# uri_onto="/home/GitHub/tabular-data-semantics-py/TabularSemantics/ontologies/schema.org.owl"

onto_access = OntologyAccess(uri_onto)
onto_access = DBpediaOntology()
onto_access = SchemaOrgOntology()

onto_access.loadOntology(True)

# load questions, search using KG

def open_file(file_to_open):
    temp = open('data/' + file_to_open + '.txt', 'r')
    filename = []
    for line in temp:
        filename.append(line)  # delimit on ?
    temp.close()
    return filename

def open_file_parsed(file_to_open,delimiter):
    temp = open('data/' + file_to_open + '.txt', 'r')
    filename = []
    for line in temp:
        filename.append(line.split(delimiter))  # delimit on ?
    temp.close()
    return filename

#non-parsed
db_questions = open_file('db_arr_q')
wd_questions = open_file('wd_arr_q')

#parsed
#db_questions = open_file_parsed('db_noun_list', '],')
#wd_questions = open_file_parsed('wd_noun_list', '],')

#print('question: ', db_questions[0])
#print('question: ', wd_questions[0])

all_entities = []

# split words

# for q in db_questions:
#     ws = re.sub('\W+', ' ', q)
#     words = ws.split(' ');
#     words = list(filter(None, words))
#     limit = 1
#
#     for w in words:
#         # print('word', w)
#         #look up in DBP KG
#         dbpedia = DBpediaLookup()
#         entities = dbpedia.getKGEntities(w, limit)
#         #print("Entities from DBPedia:")
#         for ent in entities:
#             # print('entity from DBPedia', ent)
#             all_entities.append(ent)


# use entire question

for q in db_questions:
    limit = 1
    q = re.sub('\W+', ' ', q)
    print('q', q)
    dbpedia = DBpediaLookup()
    e = dbpedia.getKGEntities(q,5)

    print('e', e)
    for ent in e:
        # print('entity from DBPedia', ent)
        all_entities.append(ent)

'''
endpoint to find type and other members of that type
'''

# #shorten array for testing
# all_entities = all_entities[0:1]

# dictionary to store types to count

type_counts_ID = []
type_counts_entity = []
type_counts_domain = []
type_counts_range = []

print('entities', len(all_entities))



for ent in all_entities:
    ep = DBpediaEndpoint()

    #finding types + counts

    #using ID/int
    ent2 = ent.getIdstr()
    types = ep.getAllTypesForEntity(ent2)
    # print('all types for entity using endpoint id', len(types), types, '\n')
    for t in types: #just retrieve one type
        type_counts_ID.append(t)
        break

    #using entity
    cls = ent.getTypes() # ont
    # print('all types using entity', cls)
    for t in cls: #just retrieve one type
        type_counts_entity.append(t)
        break

    # using predicates + ID
    predicatesForSubject = ep.getPredicatesForSubject(ent2, 1)
    # for p in predicatesForSubject:
       # print('predicates for subject using ID', p)

    predicatesForObject = ep.getPredicatesForObject(ent2, 1)
    # for p in predicatesForObject:
       # print('predicates for object using ID', p)

    types_domain = ep.getTopTypesUsingPredicatesForSubject(ent2, 1)
    for t in types_domain:
        # print('domain types: top types using predicates for subject', t)
        type_counts_domain.append(t)

    types_range = ep.getTopTypesUsingPredicatesForObject(ent2, 1)
    for t in types_range:
        # print('range types: top types using predicates for object', t)
        type_counts_range.append(t)

def count_it(list):
    counts = dict()
    for i in list:
      counts[i] = counts.get(i, 0) + 1
    return counts

type_counts_ID_fin = count_it(type_counts_ID)
type_counts_entity_fin = count_it(type_counts_entity)
type_counts_domain_fin = count_it(type_counts_domain)
type_counts_range_fin = count_it(type_counts_range)

print(type_counts_ID_fin)
print(type_counts_entity_fin)
print(type_counts_domain_fin)
print(type_counts_range_fin)

