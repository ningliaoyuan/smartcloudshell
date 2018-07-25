import json
import re

abbrDic = None
with open('data/abbr.json') as f:
    abbrDic = json.load(f)

def combineQueryRewriters(qr1, qr2):
    def combined(query):
        r1 = qr1(query)
        c = r1['corrections'] if r1['corrections'] is not None else {}
        r2 = qr2(r1['query'])
        c2 = r2['corrections'] if r2['corrections'] is not None else {}
        for key in c2:
            c[key] = c2[key]
        return {
            'query': r2['query'],
            'corrections': c
        }
    return combined

def rewriteAbbrInQuery(input, dic = None):
    if input is None:
        return input

    if dic is None:
      dic = abbrDic

    tokens = re.split(r'(\W+)',input)
    result = []
    corrections = {}
    for token in tokens:
        tokenLower = token.lower()
        if tokenLower in dic:
            word = abbrDic[tokenLower]
            result.append(word['word'])
            corrections[token] = word
        else:
            result.append(token)

    return {
        'query': ''.join(result),
        'corrections': corrections
    }

sourceTypoDic = None
with open('data/source_typos.json') as f:
    sourceTypoDic = json.load(f)

def rewriteKnownTyposInQuery(input):
    if input is None:
        return input

    result = input
    tokens = re.split(r'(\W+)',input)
    for token in tokens:
        tokenLower = token.lower()
        if tokenLower in sourceTypoDic:
            word = sourceTypoDic[tokenLower]
            result = re.sub(tokenLower, word, input, flags=re.I)
    return result
