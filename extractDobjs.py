import spacy
from spacy.lang.en import English
from spacy.symbols import nsubj, VERB, dobj
from spacy.tokens import Doc, Span, Token
from utility.NlpWithAzureResourceRecognizer import NlpWithAzureResourceRecognizer
from utility.QueryRewriter import rewriteAbbrInQuery
from utility.SpellChecker import correctSpellingErrors
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
    # output(doc)
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


ignoredDeps = [
    "advmod", #副词修饰符, what, how
    "aux", #非主要动词, to
    "advmod", # very
    "amod", # stable
    "det" #determiner
    ]
ignoredDepDic = {}
for tag in ignoredDeps:
    ignoredDepDic[tag] = True


def extractDobj2(inputText):
    text = inputText.lower()
    text = rewriteAbbrInQuery(text)['query']
    text = correctSpellingErrors(text)['query']
    doc = nlp(text)
    # output(doc)
    result = []
    for token in doc:
        # print(token.text, token.lemma_, "tag_"+token.tag_, "dep_"+token.dep_, token.head.text, token.head.pos_)
        # if token.dep_ == 'dobj' and token._.is_azure_resource:
        #     dobjs.append(token.head.text + " " + token.text)
        text = token.text
        dep = token.dep_

        if(token._.is_azure_resource):
            result.append(text)
        if dep in ignoredDepDic:
            continue
        elif token.lemma_ == "-PRON-":
            continue
        elif " " in text:
            result.append(text)
        elif text == "data":
            result.append(text)
        else:
            result.append(token.lemma_)

    return ' '.join(result)


def run():
    # extractDobj2(u"show me the firewall rule of my data lake")
    # extractDobj2(u"manage keyvault certificate")

    output = open('temp\dobjtest.txt', 'w')
    cases = getCases()
    for case in cases:
        dobj = extractDobj2(case)
        if dobj == case:
              thefile.write("%s\n" % item)
            print("======", case)
        elif dobj == None:
            print("!!!!!!", case)
        else:
            print(case, "|", dobj)


run()
