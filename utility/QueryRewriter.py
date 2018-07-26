import json
import re

abbrDic = None
with open('data/abbr.json') as f:
    abbrDic = json.load(f)
    flatAbbrDic = {key: val["word"] for key, val in abbrDic.items()}


def combineQueryRewriters(qrs):
    def combined(query):
        c = {}
        for qr in qrs:
            r = qr(query)
            query = r['query']
            if r['corrections'] is not None:
                c.update(r['corrections'])

        return {
            'query': query,
            'corrections': c
        }

    return combined


def rewriteAbbrInQuery(input, dic=None):
    if input is None:
        return input

    if dic is None:
        dic = flatAbbrDic

    tokens = re.split(r'(\W+)', input)
    result = []
    corrections = {}
    for token in tokens:
        tokenLower = token.lower()
        if tokenLower in dic:
            word = dic[tokenLower]
            result.append(word)
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
    tokens = re.split(r'(\W+)', input)
    for token in tokens:
        tokenLower = token.lower()
        if tokenLower in sourceTypoDic:
            word = sourceTypoDic[tokenLower]
            result = re.sub(tokenLower, word, input, flags=re.I)
    return result


# The default stop word list is from: https://github.com/apache/lucene-solr/blob/53981795fd73e85aae1892c3c72344af7c57083a/lucene/core/src/java/org/apache/lucene/analysis/standard/StandardAnalyzer.java#L44-L50
stopWords = ["a", "an", "and", "are", "as", "at", "be", "but", "by",
              "for", "if", "in", "into", "is", "it",
              "no", "not", "of", "on", "or", "such",
              "that", "the", "their", "then", "there", "these",
              "they", "this", "to", "was", "will", "with"]
stopWords.extend(["azure", "a", "the", "my", "me", "his",
                  "her", "what", "how", "to", "this", "that", "new"])

stopWordDic = dict((k.lower(), True) for k in stopWords)


def rewriteStopWords(input):
    if input is None:
        return input

    tokens = re.split(r'(\W+)', input)
    result = []
    corrections = {}
    stopAppendSpace = True
    for token in tokens:
        tokenLower = token.lower()
        if tokenLower in stopWordDic:
            corrections[token] = ''
        elif tokenLower == ' ':
            if stopAppendSpace == False:
                result.append(token)
            stopAppendSpace = True
        else:
            result.append(token)
            stopAppendSpace = False

    return {
        'query': ''.join(result),
        'corrections': corrections
    }