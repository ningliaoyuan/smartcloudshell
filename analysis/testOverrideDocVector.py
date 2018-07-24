import json
import spacy
import numpy as np

nlp = spacy.load('en_core_web_lg')
doc1 = nlp(u"this is text 1")
doc2 = nlp(u"I like apple")
doc1.vector = np.ones(300,)
doc2.vector = np.ones(300,)

print(doc1.similarity(doc2))

doc2.vector = np.zeros(300,) + 0.5
print(doc1.similarity(doc2))

print("completed")