import json
import spacy
import numpy
from spacy import displacy
from pprint import pprint
from pathlib import Path
import re
from spacy.vocab import Vocab

nlp = spacy.load('en_core_web_lg')

def test(text):
    print(text)
    doc = nlp (text)
    for token in doc:
        if token.is_oov:
            print('  ', token, token.is_oov)

def run():
    test(u'Delete a root certificate')
    test(u'Her ankle caught on a root, and she almost lost her balance.')
    test(u'Gets the number of nodes in each state')
    test(u'Who is number 1')
    test(u'What is the room number?')

    # azureResourceRecognizer = AzureResourceRecognizer(nlp)
    # nlp.add_pipe(azureResourceRecognizer, last=True)

    # vocab = nlp.vocab
    # docdbVector = numpy.random.uniform(-1, 1, (300,))
    # vocab.set_vector(u'docdb', docdbVector)
    # vocab.set_vector(u'cosmosdb', docdbVector)

    # print(nlp(u"how to create docdb").similarity(nlp(u"how to create cosmosdb"))) #0.9999999891092796 (random)
    # print(nlp(u"how to create docdb").similarity(nlp(u"how to create vm"))) #0.7229798838968554 (random)

    # print(nlp(u"how to create dla").similarity(nlp(u"how to create data lake analytics"))) #0.8646730444637758
    # vocab.set_vector(u'data lake analytics', vocab.get_vector(u'dla'))
    # print(nlp(u"how to create dla").similarity(nlp(u"how to create data lake analytics"))) #0.9999999205008104

run()
