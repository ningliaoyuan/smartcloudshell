import json
import spacy
from pprint import pprint
import re


def addHelpToTexts(help, allTexts):
    if help is not None:
        allTexts.append(help)


def addParametersToTexts(parameters, allTexts):
    if parameters is not None:
        for key in parameters:
            parameter = parameters[key]
            help = parameter['help']
            if help is not None:
                if(help != "==SUPPRESS=="):
                    allTexts.append(help)
    return


def addExamplesToTexts(examples, allTexts):
    if examples is not None:
        i = 0
        while i < len(examples):
            if(i % 2 == 0):
                example = examples[i]
                if(isinstance(example, list)):
                    addExamplesToTexts(example, allTexts)
                else:
                    allTexts.append(examples[i])
            i += 1
    return


def getAllTexts(file, includeHelp, includeParameters, includeExamples):
    allTexts = []
    with open(file) as f:
        data = json.load(f)
        for key in data:
            # if(key == 'network vnet check-ip-address'):
            #     pprint(key)

            cmd = data[key]
            if includeHelp and 'help' in cmd:
                help = cmd['help']
                addHelpToTexts(help, allTexts)
            if includeParameters and 'parameters' in cmd:
                parameters = cmd['parameters']
                addParametersToTexts(parameters, allTexts)
            if includeExamples and 'examples' in cmd:
                examples = cmd['examples']
                addExamplesToTexts(examples, allTexts)
    return allTexts


def writeToFile(fileName, allTexts):
    with open(fileName, "w") as text_file:
        # text_file.writelines(allTexts)
        i = 0
        length = len(allTexts)
        while i < length:
            text = allTexts[i]
            text_file.write(text + '\n')
            print('{}/{}'.format(i, length))
            i += 1
    return


def outputWords(fileName, allTexts):
    nlp = spacy.load('en_core_web_lg')
    i = 0
    csv = []
    csv.append("text, lemma_, pos_, tag_, dep_, is_alpha, is_stop, text")
    length = len(allTexts)
    while i < length:
        text = allTexts[i]
        print('{}/{} {}'.format(i, length, text))
        text = re.sub(r'\W+', ' ', text)
        doc = nlp(text)
        for token in doc:
            print(token.text, token.lemma_, token.pos_, token.tag_,
                  token.dep_, token.is_alpha, token.is_stop)
            csv.append('{},{},{},{},{},{},{},{}'.format(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.is_alpha, token.is_stop, text))
        i += 1
    writeToFile(fileName, csv)

class Word:
  def __init__(self, word, lemma, pos, tag, dep, isAlpha, isStop, text):
    self.word = word
    self.lemma = lemma
    self.pos = pos
    self.tag = tag
    self.dep = dep
    self.isAlpha = isAlpha
    self.isStop = isStop
    self.count = 1
    self.samples = [text]

def outputWordCounts(fileName, allTexts):
    nlp = spacy.load('en_core_web_lg')
    i = 0
    length = len(allTexts)
    words = {}
    while i < length:
        text = allTexts[i]
        print('{}/{} {}'.format(i, length, text))
        text = re.sub(r'\W+', ' ', text)
        doc = nlp(text)
        for token in doc:
            key = token.lemma_
            if key in words:
                words[key].count += 1
                samples = words[key].samples
                if(len(samples)<2):
                    samples.append(text)
            else:
                words[key] = Word(key, token.lemma_, token.pos_, token.tag_, token.dep_, token.is_alpha, token.is_stop, text)
        i += 1

    csv = []
    csv.append("text, lemma_, pos_, tag_, dep_, is_alpha, is_stop, count, samples")
    for key in words:
        word = words[key]
        csv.append('{},{},{},{},{},{},{},{},{}'.format(key, word.lemma, word.pos, word.tag, word.dep, word.isAlpha, word.isStop, word.count, word.samples))

    writeToFile(fileName, csv)


def run():
    # allTexts = getAllTexts('../data/help_dump.json', True, True, True)
    # writeToFile("all-text.txt", allTexts)
    # outputWords("all-words.csv", allTexts)
    # outputWordCounts("all-word-counts.csv", allTexts)

    allTexts = getAllTexts('../data/help_dump.json', True, False, True)
    writeToFile("help+sample-text.txt", allTexts)
    outputWords("help+sample-words.csv", allTexts)
    outputWordCounts("help+sample-word-counts.csv", allTexts)

    allTexts = getAllTexts('../data/help_dump.json', True, False, False)
    writeToFile("help-text.txt", allTexts)
    outputWords("help-words.csv", allTexts)
    outputWordCounts("help-word-counts.csv", allTexts)

run()
print('completed')
