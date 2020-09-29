''' author: Eleanor Bill @eljne '''
''' create vectors for additional training data - +ve '''

from kg.EB_classes import pickl, unpickle, nouns_list, noun_phrases_list, get_entities_list, apply_endpoint_list
import pandas as pd

pos = unpickle('training_vectors/10_train_new_positive_samples')
df_positive = pd.DataFrame(pos)

'''reformat to create new positive samples with similar entities'''


def new_samples(row_column):
    df = pd.DataFrame()
    entity_list = row_column['similar_entities']
    if len(entity_list) > 0:
        entity_list = list(entity_list[0])
        for indx in range(len(entity_list)):  # iterate through similar entities
            entity = entity_list[indx]
            new_row = {"category": row_column['category'],
                       "type": row_column['type'],
                       "question": row_column['question'],
                       "wh": row_column['wh'],
                       "id": row_column['id'],
                       "entity": entity,
                       "polarity": "1",
                       "noun list": row_column['noun list'],
                       "np list": row_column['np list']
                       }
            df = df.append(new_row, ignore_index=True)
    else:
        return df
    return df


# convert similar entities into new samples in dataframe
new_positive_samples = pd.DataFrame(columns=['category', 'type', 'question', 'wh', 'id', 'entity', 'polarity', 'np list', 'noun list'])

for i in range(len(df_positive)):  # iterate through questions
    positive_samples = new_samples(df_positive.loc[i])  # create new row for each similar entity - df of length 100
    new_positive_samples = new_positive_samples.append(positive_samples)  # append to overall df
    print("question", i, "/", len(df_positive), new_positive_samples.shape)

print('samples created')

print('test', new_positive_samples)

pickl('training_vectors/11_train_new_positive_samples', new_positive_samples)
print('pickled')
