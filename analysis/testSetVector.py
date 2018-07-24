import spacy
import numpy as np

nlp = spacy.load('en_core_web_md')
vocab = nlp.vocab
vector = np.zeros(300,)
vocab.set_vector('thisisoovword', vector) #throws
print('completed')
