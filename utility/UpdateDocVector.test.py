import spacy
from AzureResourceRecognizer import AzureResourceRecognizer
from UpdateDocVector import updateDocVector
from QueryRewriter import rewriteQuery


def similarity(nlp1, nlp2, text1, text2):
    doc1 = nlp1(rewriteQuery(text1))
    doc2 = nlp1(rewriteQuery(text2))
    print('1', doc1.similarity(doc2), text1,  '|', text2)

    updateDocVector(doc1)
    updateDocVector(doc2)
    print('2', doc1.similarity(doc2), text1,  '|', text2)

    doc1 = nlp2(rewriteQuery(text1))
    doc2 = nlp2(rewriteQuery(text2))
    print('3', doc1.similarity(doc2), text1, '|', text2)


def run():
    nlp = spacy.load('en_core_web_lg')
    nlp2 = spacy.load('en_core_web_lg')
    azureResourceRecognizer = AzureResourceRecognizer(nlp)
    nlp.add_pipe(azureResourceRecognizer, last=True)

    similarity(nlp, nlp2, u'turn off vm', u'vm stop')
    similarity(nlp, nlp2, u'turn off vm', u'lab vm stop')


run()
