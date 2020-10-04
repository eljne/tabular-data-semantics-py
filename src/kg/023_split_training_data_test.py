''' author: Eleanor Bill @eljne '''
''' require splitting original training data into training and test data as it's the
data we have with correct types + categories, can measure accuracy '''
from kg.EB_classes import unpickle, pickl

training_data = unpickle('training_vectors/final_original_training_vectors')
training_data2 = training_data.sample(frac=0.8, random_state=1)
testing_data = training_data.drop(training_data2.index)

training_data3 = training_data2.reset_index(drop=True)
testing_data2 = testing_data.reset_index(drop=True)

pickl('training_vectors/final_original_training_vectors_minus_tests', training_data3)
pickl('testing_vectors/11_testing_vectors_from_og_training_data', testing_data2)


