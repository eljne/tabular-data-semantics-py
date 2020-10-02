''' require splitting original training data into training and test data as it's the
data we have with correct types + categories, can measure accuracy '''
from kg.EB_classes import unpickle, pickl

training_data = unpickle('training_vectors/final_original_training_vectors')
training_data2 = training_data.sample(frac=0.8, random_state=1)
testing_data = training_data.drop(training_data2.index)

pickl('training_vectors/final_original_training_vectors_minus_tests', training_data2)
pickl('testing_vectors/11_testing_vectors_from_og_training_data', testing_data)


