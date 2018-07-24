import json
import re

abbrDic = None
with open('data/abbr.json') as f:
    abbrDic = json.load(f)

def rewriteAbbrInQuery(input):
    if input is None:
        return input

    tokens = re.split(r'(\W+)',input)
    result = []
    for token in tokens:
        tokenLower = token.lower()
        if tokenLower in abbrDic:
            word = abbrDic[tokenLower]
            result.append(word['word'])
        else:
            result.append(token)

    return ''.join(result)

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
