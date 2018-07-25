import spacy
from spacy.lang.en import English
from spacy.symbols import nsubj, VERB, dobj
from spacy.tokens import Doc, Span, Token
from NlpWithAzureResourceRecognizer import NlpWithAzureResourceRecognizer
from QueryRewriter import rewriteAbbrInQuery
from SpellChecker import correctSpellingErrors
from spacy import displacy
from pathlib import Path

import csv
import json
import os
import yaml


def getCases():
    with open('measure/testset/queries.csv') as csvfile:
        cases = []
        queries = csv.reader(csvfile)
        for row in queries:
            if len(row) == 0:
                continue

            cases.append(row[0])

    return cases


nlpWithAzureResourceRecognizer = NlpWithAzureResourceRecognizer()
nlp = nlpWithAzureResourceRecognizer.load()


def extractDobj(inputText):
    text = inputText.lower()
    text = rewriteAbbrInQuery(text)['query']
    text = correctSpellingErrors(text)['query']
    doc = nlp(text)
    output(doc)
    found = False
    dobjs = []
    for token in doc:
        if token.dep_ == 'dobj' and token._.is_azure_resource:
            dobjs.append(token.head.text + " " + token.text)

        # print(token.text, token.tag_, token.dep_, token.head.text, token.head.pos_)
        # for child in token.children:
        #     print("----", child.text, child.tag_, child.dep_, child.head.text, child.head.pos_)

    # for np in doc.noun_chunks:
    #     if np.root.dep_ == 'dobj':
    #         # print(np.root.head.text, "|", np.text, "|", np.root.text, "|", np.root.dep_)
    #         dobjs.append(np.root.head.text + " " + np.root.text)

    # TODO
    if(len(dobjs) == 1):
        return dobjs[0]

    return None


def output(doc):
    svg = displacy.render(doc, style='dep')
    file_name = '-'.join([w.text for w in doc if not w.is_punct]) + '.svg'
    output_path = Path('temp/' + file_name)
    output_path.open('w', encoding='utf-8').write(svg)


def run():
    extractDobj(u"turn off vm")
    # extractDobj(u"Add a Web App")

    cases = getCases()
    for case in cases:
        dobj = extractDobj(case)
        if dobj == case:
            print("======", case)
        elif dobj == None:
            print("!!!!!!", case)
        else:
            print(case, "|", dobj)


run()
