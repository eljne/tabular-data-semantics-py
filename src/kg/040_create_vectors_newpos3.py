''' author: Eleanor Bill @eljne '''
''' create vectors for additional training data - +ve - CONTINUED'''

# section 2
from kg.EB_classes import unpickle, pickl
from kg.EB_classes import cal_average, find_vector_kge
from gensim.models import KeyedVectors
import numpy as np

new_positive_samples = unpickle('df_positive')
print('unpickled')

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


new_positive_samples['new we_nouns_vector'] = new_positive_samples['new nouns'].apply(find_vector_we)
print('done 6')
new_positive_samples['new avg we_nouns_vector'] = new_positive_samples['new we_nouns_vector'].apply(cal_average)
print('done 7')
new_positive_samples['new we_np_vector'] = new_positive_samples['new nps2'].apply(find_vector_we)
print('done 8')
new_positive_samples['new avg we_np_vector'] = new_positive_samples['new we_np_vector'].apply(cal_average)
print('done 9')
new_positive_samples['new we_type_vector'] = new_positive_samples['new entity types'].apply(find_vector_we)
print('done 10')
new_positive_samples['new avg we_type_vector'] = new_positive_samples['new we_type_vector'].apply(cal_average)
print('done 11')

del loaded_model

new_positive_samples['new entities_KGE_vector'] = new_positive_samples['new nps2'].apply(find_vector_kge)
print('done 12')
new_positive_samples['new avg entities_KGE_vector'] = new_positive_samples['new entities_KGE_vector'].apply(cal_average)
print('done 13')

# create positive vectors

new_positive_samples['new_concatenated_vector'] = new_positive_samples.apply(lambda x: [x['we_wh_vector'],
                                                                      x['new avg we_nouns_vector'],
                                                                      x['new avg we_np_vector'],
                                                                      x['new avg entities_KGE_vector'],
                                                                      x['new avg we_type_vector']], axis=1)

pickl('df_positive_fin', new_positive_samples)

# check columns are correct
for col in new_positive_samples.columns:
    print(col)
