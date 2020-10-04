''' author: Eleanor Bill @eljne '''
''' continue creating vectors '''
''' PART 2: put parts of q through embeddings'''

from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from kg.EB_classes import find_vector_we, cal_average, type_convert, find_vector_kge
from kg.EB_classes import pickl, unpickle
import pandas as pd

stopWords = set(stopwords.words('english'))  # load stopwords
dbpedia_train_wh = unpickle('training_vectors/05_dbpedia_train_wh')

''' word embeddings on wh and nouns '''
fastTextfile = 'data/wiki-news-300d-1M.vec'
loaded_model = KeyedVectors.load_word2vec_format(fastTextfile)

# run wh through word embedding
re_list = []
for entry in dbpedia_train_wh:
    # print(entry['wh'])
    we = find_vector_we(entry['wh'], loaded_model)
    # print(we)
    entry.update({'we_wh_vector': we})
    re_list.append(entry)

dbpedia_train_wh = re_list
pickl('training_vectors/06_dbpedia_train_wh', dbpedia_train_wh)
print('done wh WE vectors found')

# run nouns through word embedding
re_list = []
for entry in dbpedia_train_wh:
    we_nouns = []
    for noun in entry['noun list']:
        we = find_vector_we(noun, loaded_model)
        if len(we) > 0:  # removed zeroed vectors to avoid affecting average
            we_nouns.append(we)
    average_vector = cal_average(we_nouns)
    entry.update({'we_nouns_vector': average_vector})
    re_list.append(entry)

dbpedia_train_wh = re_list
pickl('training_vectors/07_dbpedia_train_wh', dbpedia_train_wh)
print('done noun WE vectors found')

# run closest type through word embedding
re_list = []
for entry in dbpedia_train_wh:
    we_type = []
    for t in entry['entity_types']:
        ty = next(iter(t))
        english_label = type_convert(ty)
        we2 = find_vector_we(english_label, loaded_model)
        if len(we2) > 0:  # removed zeroed vectors to avoid affecting average
            we_type.append(we2)
    average_vector = cal_average(we_type)
    entry.update({'we_type_vector': average_vector})
    re_list.append(entry)

del loaded_model  # delete WE model from memory
dbpedia_train_wh = re_list
pickl('training_vectors/08_dbpedia_train_wh', dbpedia_train_wh)
print('done type WE vectors found')

''' use kgvec2go KGEs '''
''' link to kg embeddings using nouns and nps to find types '''
'''# Use pre-trained kg embeddings and concatenate or average them to create the vector for the question.'''

# run noun phrases through kg embedding to get vectors
re_list = []
for entry in dbpedia_train_wh:
    kge_entities = []
    for noun_phrase in entry['np list']:
        kge = find_vector_kge(noun_phrase)
        if len(kge) > 1:
            kge_entities.append(kge)
    average_vector = cal_average(kge_entities)
    entry.update({'entities_KGE_vector': average_vector})
    re_list.append(entry)

print('done entities KGE vectors found')
dbpedia_train_wh2 = re_list
pickl('training_vectors/09_dbpedia_train_wh', dbpedia_train_wh)

df = pd.DataFrame(dbpedia_train_wh2)
print(df.head())

print('ALL done pickled')