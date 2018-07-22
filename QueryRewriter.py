import json
import re

abbrDic = None
with open('data/abbr.json') as f:
    abbrDic = json.load(f)

def rewriteQuery(input):
    if input is None:
        return input

    tokens = re.split('(\W+)',input)
    result = []
    for token in tokens:
        tokenLower = token.lower()
        if tokenLower in abbrDic:
            word = abbrDic[tokenLower]
            result.append(word['word'])
        else:
            result.append(token)

    return ''.join(result)