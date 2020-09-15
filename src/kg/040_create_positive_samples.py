''' augment positive samples to create more positive sample '''
# 14th september - ejb

import pandas as pd
from kg.EB_classes import pickl, unpickle
from matching.kg_matching import Endpoint, Lookup
from ontology.onto_access import OntologyAccess, DBpediaOntology, SchemaOrgOntology

# unpickle
load = unpickle('df')
df_positive = pd.DataFrame(load)
df_positive['polarity'] = "1"

'''create more positive samples
do this by:
- getting a different but similar entity using SPARQLEndpoint
'''

onto_access = DBpediaOntology()
onto_access.loadOntology(True)


# need to get classes first
def get_classes(phrases):
    lis = []
    for ph in phrases:
        if ph != "''":
            print(ph)
            classes = onto_access.getClassIRIsContainingName(ph)
            for cls in classes:
                print(ph, 'contained by: ', cls)
                lis.append(cls)
    return lis


def get_alt_entities(entity_typess):
    lis = []
    for ls in entity_typess:
        for enty in ls:
            # ep = Endpoint()
            print('enty', enty)
            if "dbpedia" in enty:
                simty = ep.getEntitiesForDBPediaClass(enty, 3)
                for e in simty:
                    print(enty, 'relates to: ', e)
                    lis.append(e)
    return lis


df_positive['similar_entities'] = df_positive['entity_types'].apply(get_alt_entities)   # column by column
print('done got similar entities')

# separate positive and negative samples
df_positive_final = df_positive[["category",
                                  "type",
                                  "question",
                                  "wh",
                                  "id",
                                  "similar_entities",
                                 "polarity"
                                  ]]    # subset of df

# pickle
pickl('positive_samples', df_positive_final)
print('done pickled')