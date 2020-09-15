# create vectors for additional training data - +ve and -ve
from kg.EB_classes import pickl, unpickle

# unpickle
pos = unpickle('positive_samples')
neg = unpickle('negative_samples')

print(neg.type)

# how do the new samples affect the vector?

# positive - changed entities affect nouns/noun phrases vectors
# n more sets of +ve data where n is the possible number of changed entities

# def positive(column_row):
#     for n in column_row:
#         replace entity in question/noun/np list


# negative - shuffled types and categories affect the types and
#          - sibling type affects type vectors
# 3 more sets of -ve data:

df_negative_st = neg.copy() # - shuffled type
df_negative_sc = neg.copy() # - shuffled category
df_negative_sb = neg.copy() # - sibling type


# check polarity

# append together

# pickle new training data
# pickl('new_td', new_td)
