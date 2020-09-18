''' author: Eleanor Bill @eljne '''
''' augment positive samples to create more positive sample '''
# takes about 6 hours to run

import pandas as pd
from kg.EB_classes import pickl, unpickle
from matching.kg_matching import Endpoint
from ontology.onto_access import DBpediaOntology

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
ep = Endpoint()


def get_alt_entities(entity_typess):
    lis = []
    for ls in entity_typess:
        for enty in ls:
            if "dbpedia" in enty:
                try:
                    print('entity:', enty)
                    simty = ep.getEntitiesForDBPediaClass(enty, 1)
                    lis.append(simty)
                    print('similar entity', simty)
                except:
                    pass
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