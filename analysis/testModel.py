import json
import spacy, time
import numpy
from spacy import displacy
from pprint import pprint
from pathlib import Path
import re
from spacy.vocab import Vocab
from AzureResourceRecognizer import AzureResourceRecognizer

def run(modelFile):
    abbrDic = None
    print(modelFile)
    with open('../data/abbr.json') as f:
        abbrDic = json.load(f)
        nlp = spacy.load(modelFile)
        vocab = nlp.vocab
        oov = []
        for abbr in abbrDic:
            fullWords = abbrDic[abbr]['word']
            if abbr in vocab:
                similarity = nlp(abbr).similarity(nlp(fullWords))
                print(abbr,fullWords,similarity)
            else:
                oov.append(abbr)
        print(oov)

run('en_vectors_web_lg')
run('en_core_web_lg')
