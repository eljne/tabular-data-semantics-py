''' author: Eleanor Bill @eljne '''
''' create vectors for additional training data - +ve '''

from kg.EB_classes import pickl, unpickle, nouns_list, noun_phrases_list, get_entities_list, apply_endpoint_list
from kg.EB_classes import cal_average, find_vector_kge
from gensim.models import KeyedVectors
import numpy as np
import pandas as pd
from kg.endpoints import DBpediaEndpoint

# unpickle
pos = unpickle('positive_samples')
df_positive = pd.DataFrame(pos)

# how do the new samples affect the vector?

# positive - changed entities affect nouns/noun phrases vectors
# n more sets of +ve data where n is the possible number of changed entities
# switch out the nouns and noun phrases for the new entities in various combinations
ep = DBpediaEndpoint()


# reformat to return string associated with entity
def positive(column_row):
    entities = []
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


df_positive['new nps'] = df_positive['similar_entities'].apply(positive)    # reformat to return string associated with entity
print('done 1')
# print(df_positive['new nps'])

# filter entities into nouns and noun phrases
df_positive['new nouns'] = df_positive['new nps'].apply(nouns_list)
print('done 2')
# print(df_positive['new nouns'])
df_positive['new nps2'] = df_positive['new nps'].apply(noun_phrases_list)
print('done 3')
# print(df_positive['new nps2'])

# get entities associated with noun phrases
df_positive['new entities'] = df_positive['new nps2'].apply(get_entities_list)
print('done 4')
print(df_positive['new entities'])

# DEBUG FROM HERE

# get types associated with entities
df_positive['new entity types'] = df_positive['new entities'].apply(apply_endpoint_list)
print('done 5')
print(df_positive['new entity types'])

pickl('df_positive', df_positive)

# section 2
df_positive = unpickle('df_positive')

# get embeddings
fastTextfile = 'data/wiki-news-300d-1M.vec'
loaded_model = KeyedVectors.load_word2vec_format(fastTextfile)


# find word embedding vector
def find_vector_we(word_or_phrase):
    try:
        vector = loaded_model.word_vec(word_or_phrase)
    except:
        vector = np.zeros(1)
    return vector


df_positive['new we_nouns_vector'] = df_positive['new nouns'].apply(find_vector_we)
print('done 6')
df_positive['new avg we_nouns_vector'] = df_positive['new we_nouns_vector'].apply(cal_average)
print('done 7')
df_positive['new we_np_vector'] = df_positive['new nps2'].apply(find_vector_we)
print('done 8')
df_positive['new avg we_np_vector'] = df_positive['new we_np_vector'].apply(cal_average)
print('done 9')
df_positive['new we_type_vector'] = df_positive['new entity types'].apply(find_vector_we)
print('done 10')
df_positive['new avg we_type_vector'] = df_positive['new we_type_vector'].apply(cal_average)
print('done 11')

del loaded_model

df_positive['new entities_KGE_vector'] = df_positive['new nps2'].apply(find_vector_kge)
print('done 12')
df_positive['new avg entities_KGE_vector'] = df_positive['new entities_KGE_vector'].apply(cal_average)
print('done 13')

# create positive vectors

df_positive['new_concatenated_vector'] = df_positive.apply(lambda x: [x['we_wh_vector'],
                                                                      x['new avg we_nouns_vector'],
                                                                      x['new avg we_np_vector'],
                                                                      x['new avg entities_KGE_vector'],
                                                                      x['new avg we_type_vector']], axis=1)


pickl('df_positive_fin', df_positive)

# check columns are correct
for col in df_positive.columns:
    print(col)