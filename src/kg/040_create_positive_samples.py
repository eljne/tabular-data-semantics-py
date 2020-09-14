''' augment positive samples to create more positive sample '''
# 14th september - ejb
# may not include this after all - ask Ernesto

import pandas as pd
import pickle
import random
from ontology.onto_access import DBpediaOntology

# unpickle
pkl_file = open('data/df.pkl', 'rb')
load = pickle.load(pkl_file)
pkl_file.close()

df_positive = pd.DataFrame(load)
df_positive['polarity'] = "1"

'''create more positive samples
do this by:
- getting a different entity (sibling?) using ontology
'''

uri_onto = "http://www.cs.ox.ac.uk/isg/ontologies/schema.org.owl"
onto_access = DBpediaOntology()
onto_access.loadOntology(True)


def get_sibling(nps):
    # ['political ideology', 'nazis']
    # ['google knowledge graph id', 'martn vizcarra']
    labels = []
    for n in nps:
        try:
            # print("\n 1")
            ancestors = onto_access.getAncestorsURIs(onto_access.getClassByName(n))
            print('ancestors', ancestors)
            ancestor = random.sample(ancestors, k=1)
            # print('ancestor', ancestor[0])
            cl8ss = onto_access.getClassByURI(ancestor[0])
            siblings = onto_access.getDescendantNames(cl8ss)
            # print('siblings', siblings)
            sibling = random.sample(siblings, k=1)
            # print('sibling', sibling[0])
            while sibling[0] == t:
                 sibling = random.sample(siblings, k=1)
            labels.append(sibling[0])
        except:
            try:
                # print("\n 2")
                similar = onto_access.getClassIRIsContainingName(t2)
                labels = onto_access.getDescendantNames(similar)
                label = random.sample(labels, k=1)
                labels.append(label[0])
                # print(label[0])
            except:
                pass
    # print('\n types', types)
    # print('labels', labels)
    return labels


df_positive['sibling_entity'] = df_positive['np list'].apply(get_sibling)   # column by column
print('done siblings got for entities')

# pickle
f = open('data/positive_samples.pkl', 'wb')
pickle.dump(df_positive, f)
f.close()

print('done pickled')