''' author: Eleanor Bill @eljne '''
''' create vectors for additional training data - +ve - CONTINUED'''
''' takes about four-five hours w/10 samples per question - 180,000 '''

from kg.EB_classes import pickl, unpickle, nouns_list, noun_phrases_list
import pandas as pd
from kg.endpoints import DBpediaEndpoint

pos = unpickle('new_positive_samples')
new_positive_samples = pd.DataFrame(pos)
print('unpickled')
ep = DBpediaEndpoint()
# print(new_positive_samples.head)


def get_nouns(entity):
    labels = ep.getEnglishLabelsForEntity(entity)
    nouns = nouns_list(labels)
    print('.')
    return nouns


def get_nps(entity):
    labels = ep.getEnglishLabelsForEntity(entity)
    nps = noun_phrases_list(labels)
    print('..')
    return nps


def apply_endpoint_alt(entity):  # find types
    types = ep.getTypesForEntity(entity)  # limit to 5
    # print('types using endpoint id', types)
    if len(types) == 0:  # using entity: back up
        types = entity.getTypes()  # ont
        # print('types using entity', types, '\n')
    print('...')
    return types


new_positive_samples['additional noun list'] = new_positive_samples['entity'].apply(get_nouns)
print('done get nouns')
new_positive_samples['additional np list'] = new_positive_samples['entity'].apply(get_nps)
print('done get nps')
new_positive_samples['new entity types'] = new_positive_samples['entity'].apply(apply_endpoint_alt)
print('done get types')
pickl('new_positive_samples2', new_positive_samples)
print('pickled')
