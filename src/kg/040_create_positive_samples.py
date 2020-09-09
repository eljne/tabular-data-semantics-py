''' augment positive samples to create more positive sample '''
# 9th september - ejb
# may not include this after all - ask Ernesto

# read csv file
df = pd.read_csv('data/df.csv')

print('done read from csv')

'''test different strategies to augment positive samples'''

# query for siblings of target types
# siblings of the classes associated with the target types e.g. ‘basketball player’ vs. ‘football player’
uri_onto = "http://www.cs.ox.ac.uk/isg/ontologies/schema.org.owl"
onto_access = DBpediaOntology()
onto_access.loadOntology(True)