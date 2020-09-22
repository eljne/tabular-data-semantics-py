''' author: Eleanor Bill @eljne '''
''' create vectors for additional training data - +ve - CONTINUED'''

from kg.EB_classes import pickl, unpickle, nouns_list, noun_phrases_list, get_entities_list, apply_endpoint_list
import pandas as pd
from kg.endpoints import DBpediaEndpoint

pos = unpickle('new_positive_samples')
new_positive_samples = pd.DataFrame(pos)
print('unpickled')

print(new_positive_samples.head)

# how do the new samples affect the vector?
# changed entities affect nouns/noun phrases vectors
# n more sets of +ve data where n is the possible number of changed entities
# switch out the nouns and noun phrases for the new entities in various combinations
ep = DBpediaEndpoint()


# reformat to return string associated with entity
def positive(column_row):
    entities = []
    print(column_row)
    for n in column_row:  # clean entities (just get label)
        for a in n:
            # get label for entity
            label = ep.getEnglishLabelsForEntity(a)
            try:
                lb = label.pop()
            except:
                lb = ''
            if lb is not None or '':
                entities.append(lb)
    return entities


new_positive_samples['new nps'] = new_positive_samples['entity'].apply(positive)
# reformat to return string associated with entity
print('done 1')
# print(df_positive['new nps'])

# filter entities into nouns and noun phrases
new_positive_samples['new nouns'] = new_positive_samples['new nps'].apply(nouns_list)
print('done 2')
# print(df_positive['new nouns'])
new_positive_samples['new nps2'] = new_positive_samples['new nps'].apply(noun_phrases_list)
print('done 3')
# print(df_positive['new nps2'])

# get entities associated with noun phrases
new_positive_samples['new entities'] = new_positive_samples['new nps2'].apply(get_entities_list)
print('done 4')
print(new_positive_samples['new entities'])

# DEBUG FROM HERE

# get types associated with entities
new_positive_samples['new entity types'] = new_positive_samples['new entities'].apply(apply_endpoint_list)
print('done 5')
print(new_positive_samples['new entity types'])

pickl('new_positive_samples2', new_positive_samples)
print('pickled')
