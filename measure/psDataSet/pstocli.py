import csv
import spacy
import json
import re

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

def psCommandNamePreprocess(command):
    command = command.replace('-', ' ')
    command = command.replace('AzureRm', '')
    command = command.replace("New", "create")
    command = command.replace("Get", "get")
    command = command.replace("List", "get")
    command = command.replace("Add", "create")
    command = command.replace("Set", "update")
    command = " ".join(camel_case_split(command))
    return command

psCommands = []
azCommands = []

psCommandMatch = {}

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en_core_web_lg')
print('module loaded!')
with open('./measure/testset/helpToCommand.csv') as azFile:
    reader = csv.reader(azFile)
    for row in reader:
        azCommands.append(nlp(row[1]))
        pass
mapping = open('./measure/testset/PStoAzMapping.csv', 'wb')
with open('./measure/testset/azurePowershellCommands.csv') as psFile:
    reader = csv.reader(psFile)
    for row in reader:
        psCommand = psCommandNamePreprocess(row[2])
        psCommandDoc = nlp(psCommand)
        #print('trying to match {}'.format(psCommand))
        maxScore = 0
        maxScoreDoc = None
        for doc in azCommands:
            score = psCommandDoc.similarity(doc)
            if score > maxScore:
                maxScore = score
                maxScoreDoc = doc
                print('    better score with {} = {}'.format(doc.text, score))
        if maxScoreDoc is not None:
            print('{} match to {} with score {}'.format(psCommand, maxScoreDoc.text, maxScore))
            psCommandMatch[psCommand] = maxScoreDoc.text
            mapping.write("{} : {}\n".format(psCommand, maxScoreDoc.text).encode())

with open('psToazMapping.json', 'w') as outfile:
    json.dump(psCommandMatch, outfile)