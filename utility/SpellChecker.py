from spellchecker import SpellChecker
import re, csv, json

oovs = ["firewall"]
with open('analysis/help+sample-word-oov.csv') as oovFile:
    rows = csv.reader(oovFile)
    next(rows) # skip header line
    for row in rows:
        oovs.append(row[0])

with open('data/source_typos.json') as f:
    typos = json.load(f)
    for typo in typos.keys():
        oovs.remove(typo)

wordFrequency = {}
with open('data/word-frequencies.json') as f:
    wordFrequency = json.load(f)

spell = SpellChecker()
spell.word_frequency.load_words(oovs)

def getWordFrequency(word):
    return wordFrequency[word] if word in wordFrequency else 0

def correctSpellingErrors(input):
    if input is None:
        return input

    result = input
    wordRE = re.compile(r'^\w+$')
    tokens = filter(lambda t: wordRE.match(t), re.split(r'(\W+)',input))
    tokens = map(lambda t: t.lower(), tokens)
    corrections = {}

    for unknown in spell.unknown(tokens):
        candidates = spell.candidates(unknown)
        word = spell.correction(unknown)
        wf = getWordFrequency(word)
        for c in candidates:
            _wf = getWordFrequency(c)
            if _wf > wf:
                word = c
                wf = _wf
        result = re.sub(unknown, word, input, flags=re.I)
        corrections[unknown] = word
    return {
        'query': result,
        'corrections': corrections
    }
