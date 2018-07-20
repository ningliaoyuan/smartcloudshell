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


def getAllTexts(file):
    allTexts = []
    with open(file) as f:
        data = json.load(f)
        for key in data:
            if(key == 'network vnet check-ip-address'):
                pprint(key)

            cmd = data[key]
            if 'help' in cmd:
                help = cmd['help']
                addHelpToTexts(help, allTexts)
            if 'parameters' in cmd:
                parameters = cmd['parameters']
                addParametersToTexts(parameters, allTexts)
            if 'examples' in cmd:
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
            i+=1
    return

def run():
    allTexts = getAllTexts('../data/help_dump.json')
    # writeToFile("all-text.txt", allTexts)

    nlp = spacy.load('en_core_web_lg')
    i = 0
    while i < len(allTexts):
        text = allTexts[i]
        print(text)
        text = re.sub(r'\W+', ' ', text)
        doc = nlp(text)
        for token in doc:
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
        i += 1

run()
print('completed')
