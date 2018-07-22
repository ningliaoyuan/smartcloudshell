from __future__ import unicode_literals, print_function
import spacy
import plac
from spacy.lang.en import English
from spacy.tokens import Doc, Span, Token
from AzureResourceRecognizer import AzureResourceRecognizer

nlp = spacy.load('en_core_web_lg')

def test(text):
    doc = nlp(text)
    print('Tokens', [t.text for t in doc]) 
    # print('Doc has_azure_resource', doc._.has_azure_resource)
    # print('Token 0 is_azure_resource', doc[1]._.is_azure_resource)
    # print('Token 1 is_azure_resource', doc[2]._.is_azure_resource)
    print('Entities', [(e.text, e.label_) for e in doc.ents])

def run():
    text = "Start my virtual machine."
    test(text) # [u'Start', u'my', u'virtual', u'machine', u'.']
    azureResourceRecognizer = AzureResourceRecognizer(nlp)
    nlp.add_pipe(azureResourceRecognizer, last=True)
    test(text) # [u'Start', u'my', u'virtual machine', u'.']

run()