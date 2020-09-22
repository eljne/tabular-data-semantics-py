''' author: Eleanor Bill @eljne '''
''' create vectors for additional training data - +ve '''

from kg.EB_classes import pickl, unpickle, nouns_list, noun_phrases_list, get_entities_list, apply_endpoint_list
import pandas as pd

pos = unpickle('positive_samples')
df_positive = pd.DataFrame(pos)

'''reformat to create new positive samples with similar entities'''

# convert similar entities into new samples in dataframe
new_positive_samples = pd.DataFrame(columns=['category', 'type', 'question', 'wh', 'id', 'entity', 'polarity'])


def new_samples(row_column, df):
    entity_list = row_column['similar_entities']
    for ent in entity_list:
        for e in ent:
            new_row = pd.DataFrame({"category": row_column['category'],
                                    "type": row_column['type'],
                                    "question": row_column['question'],
                                    "wh": row_column['wh'],
                                    "id": row_column['id'],
                                    "entity": e,
                                    "polarity": row_column['polarity']
                                    })
            df = df.append(new_row, ignore_index=True)
            # print(df.shape)
    return df


# apply row by row - work out the loops
positive_samples = df_positive.apply(lambda x: new_samples(x, new_positive_samples), axis=1)
print('samples created')

print('test', new_positive_samples)

pickl('new_positive_samples', new_positive_samples)
print('pickled')
