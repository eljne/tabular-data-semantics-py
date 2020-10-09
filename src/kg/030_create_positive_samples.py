''' author: Eleanor Bill @eljne '''
''' augment positive samples to create more positive samples '''
''' about 20 mins '''

import pandas as pd
from kg.EB_classes import pickl, unpickle, get_last
from matching.kg_matching import Endpoint
from kg.endpoints import DBpediaEndpoint
from ontology.onto_access import DBpediaOntology

# unpickle
# load = unpickle('training_vectors/final_original_training_vectors') # when we have training data from task to eval
load = unpickle('training_vectors/final_original_training_vectors_minus_tests') # created own testing data from splitting train
df_positive = pd.DataFrame(load)
df_positive['polarity'] = "1"

'''create more positive samples
do this by:
- getting a different but similar entity using SPARQLEndpoint
'''

onto_access = DBpediaOntology()
onto_access.loadOntology(True)
ep = DBpediaEndpoint()    # getEntitiesForType


def get_alt_entities(entity_types):
    lis = []
    for ls in entity_types:
        # print('ls', ls)
        enty = get_last(ls)  # only get finest entity
        # print('entity:', enty)
        try:
            # simty = ep.getEntitiesForDBPediaClass(enty, 100) - slower version
            simty = ep.getEntitiesForType(enty, 0, 10)
            lis.append(simty)
            # print('similar entity', simty)
        except:
            pass
    return lis


df_positive['similar_entities'] = df_positive['entity_types'].apply(get_alt_entities)  # column by column
print('done got similar finest entities')

# separate positive and negative samples
df_positive_final = df_positive[["category",
                                 "type",
                                 "question",
                                 "wh",
                                 "id",
                                 "similar_entities",
                                 "polarity",
                                 "noun list",
                                 "np list"
                                 ]]  # subset of df

# pickle
pickl('training_vectors/10_train_new_positive_samples', df_positive_final)
print('done pickled')
