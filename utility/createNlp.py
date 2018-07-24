import json
import spacy, time
import numpy as np
from spacy import displacy
from pprint import pprint
from pathlib import Path
import re
from spacy.vocab import Vocab
from AzureResourceRecognizer import AzureResourceRecognizer

abbrDic = None
with open('../data/abbr.json') as f:
    abbrDic = json.load(f)

def getVector(vocab, words):
    tokens = words.split(' ')
    # vectors = []
    vectorsSum = np.zeros(300,)
    for token in tokens:
        vector = vocab.get_vector(token)
        vectorsSum+=vector
        # vectors.append(vocab.get_vector(token))

    average = vectorsSum / len(tokens)
    return average

def createNlp():
    nlp = spacy.load('en_core_web_lg')
    azureResourceRecognizer = AzureResourceRecognizer(nlp)
    nlp.add_pipe(azureResourceRecognizer, last=True)

    vocab = nlp.vocab
    for abbr in abbrDic:
        words = abbrDic[abbr]['word']
        vector = getVector(vocab, words)
        vocab.set_vector(abbr, vector)
        vocab.set_vector(words, vector)

    return nlp