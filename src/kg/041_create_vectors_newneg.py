''' author: Eleanor Bill @eljne '''
''' create vectors for negative samples '''

from kg.EB_classes import pickl, unpickle
from kg.EB_classes import cal_average
from gensim.models import KeyedVectors
import numpy as np

# negative - shuffled types and categories affect the types and
#          - sibling type affects type vectors
# 3 more sets of -ve data:

neg = unpickle('negative_samples')

df_negative_st = neg.copy()  # - shuffled type - change __ embeddings
df_negative_sc = neg.copy()  # - shuffled category - change __ embeddings
df_negative_sb = neg.copy()  # - sibling type - change __ embeddings
print('done copied')

# how do the new samples affect the vector?
fastTextfile = 'data/wiki-news-300d-1M.vec'
loaded_model = KeyedVectors.load_word2vec_format(fastTextfile)


# find word embedding vector
def find_vector_we(word_or_phrase):
    try:
        vector = loaded_model.word_vec(word_or_phrase)
    except:
        vector = np.zeros(1)
    return vector


# df_negative_sb - changed entity types
df_negative_sb['new we_type_vector'] = df_negative_sb['sibling_type'].apply(find_vector_we)
print('done 1')
df_negative_sb['new avg we_type_vector'] = df_negative_sb['new we_type_vector'].apply(cal_average)
print('done 2')

for col in df_negative_sb.columns:
    print(col)

df_negative_sb['concatenated_vector'] = df_negative_sb.apply(lambda x: [x['we_wh_vector'],
                                                                      x['we_nouns_vector'],
                                                                      x['we_np_vector'],
                                                                      x['entities_KGE_vector'],
                                                                      x['new avg we_type_vector']], axis=1)
print('done 3')

# df_negative_st - changed types - doesn't affect anything, just changes assigned type
# df_negative_sc - changed categories - doesn't affect anything, just changes assigned category

# append together
df_neg_all = df_negative_sb.append(df_negative_st)
df_neg_all2 = df_neg_all.append(df_negative_sc)
print('done 5')

# pickle
pickl('df_negative_fin', df_neg_all2)
print('pickled')

# check columns are correct
for col in df_neg_all2.columns:
    print(col)

'''
category 
concatenated_vector
entities_KGE_vector
id
new avg we_type_vector - rename
new we_type_vector - drop
polarity
question
shuffled_category
shuffled_type
sibling_type
type
we_nouns_vector
we_np_vector
we_wh_vector
wh
'''

