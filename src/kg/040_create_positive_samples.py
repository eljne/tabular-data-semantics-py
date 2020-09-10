''' augment positive samples to create more positive sample '''
# 9th september - ejb
# may not include this after all - ask Ernesto

import pandas as pd
import pickle

# unpickle
pkl_file = open('data/df.pkl', 'rb')
load = pickle.load(pkl_file)
pkl_file.close()

df_positive = pd.DataFrame(load)

df_positive['polarity'] = "1"

'''test different strategies to augment positive samples'''

# query for siblings of target types
# get questions with different types in them e.g. who coached [athlete]? [coach]
# siblings of the classes associated with the target types e.g. ‘basketball player’ vs. ‘football player’
# uri_onto = "http://www.cs.ox.ac.uk/isg/ontologies/schema.org.owl"
# onto_access = DBpediaOntology()
# onto_access.loadOntology(True)

# pickle
f = open('data/positive_samples.pkl', 'wb')
pickle.dump(df_positive, f)
f.close()

print('done pickled')