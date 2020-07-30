'''
Created on 19 Mar 2019
@author: ejimenez-ruiz

Edited on Jul 2020
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

# load parsed questions, search using KG

parsed_questions = open('data/db_noun_list.txt', 'r')
for line in parsed_questions:
    db_questions = line.split('],')  # delimit on ?
parsed_questions.close()

parsed_questions = open('data/wd_noun_list.txt', 'r')
for line in parsed_questions:
    wd_questions = line.split('],')  # delimit on ?
parsed_questions.close()

print('question', db_questions[0])
# print(wd_questions[0])

all_entities = []
db_questions = db_questions[0:1]

for q in db_questions:
    ws = re.sub('\W+', ' ', q)
    words = ws.split(' ');
    words = list(filter(None, words))
    limit = 1

    for w in words:
        print('word', w)
        #look up in DBP KG
        dbpedia = DBpediaLookup()
        entities = dbpedia.getKGEntities(w, limit)
        #print("Entities from DBPedia:")
        for ent in entities:
            print('entity from DBPedia', ent)
            all_entities.append(ent)


'''
endpoint to find type and other members of that type
'''

# #shorten array for test
all_entities = all_entities[0:1]
type_counts = {} # dictionary to store types to count

for ent in all_entities:
    print('ent id', ent.getId())
    print('ent idstr', ent.getIdstr())
    print('ent type', ent.getTypes())
    print('ent label', ent.getLabel())
    print('ent source', ent.getSource())

    ep = DBpediaEndpoint()

    #finding types

    #using ID/int
    ent2 = ent.getIdstr()
    types = ep.getAllTypesForEntity(ent2)
    print('all types for entity using endpoint id', len(types), types, '\n')

    #using entity
    cls = ent.getTypes() # ont
    print('all types using entity',cls)

    # get predicates using ID

    predicatesForSubject = ep.getPredicatesForSubject(ent2, 10)
    for p in predicatesForSubject:
       print('predicates for subject using ID', p)

    predicatesForObject = ep.getPredicatesForObject(ent2, 10)
    for p in predicatesForObject:
       print('predicates for object using ID', p)

    print("Domain types")
    types_domain = ep.getTopTypesUsingPredicatesForSubject(ent2, 3)
    for t in types_domain:
        print('top types using predicates for subject', t)

    print("Range types")
    types_range = ep.getTopTypesUsingPredicatesForObject(ent2, 3)
    for t in types_range:
        print('top types using predicates for object', t)

    labels = []

    # get class siblings to create additional training data

    for c in cls: #for each class
        print('c', c)
        entities2 = ep.getEntitiesForType(c, 0, 5)
        print('entities for types from original entity', entities2) #http://dbpedia.org/resource/Axel_Anderberg

        entities_labels = ep.getEntitiesLabelsForType(c, 0, 5)
        for e, label in entities_labels.items():
            print('ent', e, 'label', label)
            label = str(label)
            label = re.sub('}','', label)
            label = re.sub('{', '', label)
            label = re.sub('\'', '\"', label)
            labels.append(label)

        # class_labels = ep.createSPARQLEntitiesLabelsForClass(c,0,5)
        # print('class labels', class_labels)
        # for lb in class_labels:
        #     print('class label', lb)
        #     print('test', onto_access.getClassByName(lb))
        #     print('test', onto_access.getClassByName(lb).descendants())
        #     print('test', onto_access.getClassByName(lb).ancestors())

        eq_class = ep.getEquivalentClasses(c)
        for cl in eq_class:
            print('equivalent classes', cl)

        sup2dist = ep.getDistanceToAllSuperClasses(c)
        print('distance to sup', len(sup2dist), sup2dist)

        sub2dist = ep.getDistanceToAllSubClasses(c)
        print('distance to sub', len(sub2dist), sub2dist)

        '''
        OntologyAccess to find classes 
        '''

        # OntologyAccess
        # a way to get classes
        # getClassByURI
        # getOntology

    # get classes and related
    # print('test', onto_access.getClassByURI(""))
    # print('test', onto_access.getClassByURI("").descendants())
    # print('test', onto_access.getClassByURI("").ancestors())
    # print('test', onto_access.getDescendantURIs(onto_access.getClassByName("City")))
    # print('test', onto_access.getAncestorsURIs(onto_access.getClassByName("City")))

#wikidata

        #look up in WD KG
        # wikidata = WikidataAPI()
        # entities = wikidata.getKGEntities(w, limit)
        # print("Entities from Wikidata:")
        # for ent in entities:
        #     print(ent)
        # print("\n")

    # ep = WikidataEndpoint()
    # types = ep.getAllTypesForEntity("http://www.wikidata.org/entity/Q22")
    # print(len(types), types)

    # equiv = ep.getEquivalentClasses(c)
    # print(len(equiv), equiv)

    # same = ep.getSameEntities(ent2)
    # print(len(same), same)

    # gt_cls = "http://www.wikidata.org/entity/Q5"
    # sup2dist = ep.getDistanceToAllSuperClasses(gt_cls)
    # print(len(sup2dist), sup2dist)
    #
    # sub2dist = ep.getDistanceToAllSubClasses(gt_cls, 2)
    # print(len(sub2dist), sub2dist)

