import json
import re

abbrDic = None
with open('data/abbr.json') as f:
    abbrDic = json.load(f)

def rewriteQuery(input, dic = None):
    if input is None:
        return input

    if dic is None:
      dic = abbrDic

    tokens = re.split(r'(\W+)',input)
    result = []
    for token in tokens:
        tokenLower = token.lower()
        if tokenLower in dic:
            word = abbrDic[tokenLower]
            result.append(word['word'])
        else:
            result.append(token)

    return ''.join(result)
