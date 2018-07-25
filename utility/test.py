import spacy
import plac
from spacy.lang.en import English
from spacy.tokens import Doc, Span, Token
from AzureResourceRecognizer import AzureResourceRecognizer
from QueryRewriter import rewriteAbbrInQuery, rewriteKnownTyposInQuery
from UpdateDocVector import updateDocVector

nlp = spacy.load('en_core_web_lg')
nlp2 = spacy.load('en_core_web_lg')

azureResourceRecognizer = AzureResourceRecognizer(nlp)
nlp.add_pipe(azureResourceRecognizer, last=True)

testcases = [
    u"create vm",
    u"create virtual machine",
    u"create dla",
    u"create data lake analytics",
    u"delete sf",
]


def test(text1, text2):
    text1 = rewriteAbbrInQuery(text1)
    text2 = rewriteAbbrInQuery(text2)
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    # similarity = doc1.similarity(doc2)
    # print('a', similarity, text1, "|", text2)

    updateDocVector(doc1)
    updateDocVector(doc2)

    similarity = doc1.similarity(doc2)
    print('b', similarity, text1, "|", text2)

    doc1 = nlp2(text1)
    doc2 = nlp2(text2)
    similarity = doc1.similarity(doc2)
    print('c', similarity, text1, "|", text2)

# test(u'get active directory Service Principal Credential', u'provider operation list')
# test(testcases[1], testcases[2])
test(u'create windows 10 vmss', 'vmss create')
# test(u'get active directory Service Principal Credential', u"ad sp credential list")
