''' author: Eleanor Bill @eljne '''
''' create vectors for additional training data - +ve - CONTINUED'''
'''quick!'''

from kg.EB_classes import unpickle, pickl
from kg.EB_classes import cal_average, find_vector_kge
from gensim.models import KeyedVectors
import numpy as np

new_positive_samples = unpickle('new_positive_samples2')
print('unpickled')
# new_positive_samples = pd.DataFrame(new_positive_samples)

new_positive_samples['new nps2'] = new_positive_samples['np list'] + new_positive_samples['additional np list']
new_positive_samples['new nouns'] = new_positive_samples['noun list'] + new_positive_samples['additional noun list']
print('new fields created')

# get pre-trained word embeddings
fastTextfile = 'data/wiki-news-300d-1M.vec'
loaded_model = KeyedVectors.load_word2vec_format(fastTextfile)
print('models loaded')


# find word embedding vector
def find_vector_we(word_or_phrase):
    try:
        vector = loaded_model.word_vec(word_or_phrase)
    except:
        vector = np.zeros(1)
    print('.')
    return vector


new_positive_samples['we_wh_vector'] = new_positive_samples['wh'].apply(find_vector_we)
print('done 0')
new_positive_samples['new we_nouns_vector'] = new_positive_samples['new nouns'].apply(find_vector_we)
print('done 1')
new_positive_samples['new avg we_nouns_vector'] = new_positive_samples['new we_nouns_vector'].apply(cal_average)
print('done 2')
new_positive_samples['new we_type_vector'] = new_positive_samples['new entity types'].apply(find_vector_we)
print('done 5')
new_positive_samples['new avg we_type_vector'] = new_positive_samples['new we_type_vector'].apply(cal_average)
print('done 6')

del loaded_model

new_positive_samples['new entities_KGE_vector'] = new_positive_samples['new nps2'].apply(find_vector_kge)
print('done 7')
new_positive_samples['new avg entities_KGE_vector'] = new_positive_samples['new entities_KGE_vector'].apply(cal_average)
print('done 8')

pickl('df_positive_fin1', new_positive_samples)
print('done pickled 1')

# create positive vectors
new_positive_samples['new_concatenated_vector'] = new_positive_samples.apply(lambda x: [x['we_wh_vector'],
                                                                                        x['new avg we_nouns_vector'],
                                                                                        x['new avg entities_KGE_vector'],
                                                                                        x['new avg we_type_vector']],
                                                                             axis=1)

pickl('df_positive_fin2', new_positive_samples)
print('done pickled 2')
