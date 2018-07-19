import spacy, time
from data import getAllCommandsWithHelpAsQuery, getAllCommandsWithCommandAsQuery

# Load English tokenizer, tagger, parser, NER and word vectors
# https://spacy.io/usage/models

import en_core_web_lg as model

print("loading model from en_core_web_lg")
ts = time.time()

nlp = model.load()

print("loaded, elapsed time:", time.time() - ts)

def process(cmd):
  try:
    cmd['nlp'] = nlp(cmd['query'])
  except:
    print('Error occurred to ' + cmd['id'])
  return cmd

print("calculating command/help vectors")
ts = time.time()
helpCommands = getAllCommandsWithHelpAsQuery()
helpCommandNodes = list(map(lambda c: process(c), helpCommands))
print("done, elapsed time:", time.time()-ts)

print("calculating command/command vectors")
ts = time.time()
commands = getAllCommandsWithCommandAsQuery()
commandNodes = list(map(lambda c: process(c), commands))
print("done, elapsed time:", time.time()-ts)

def compare(inputStr):
  input = nlp(inputStr)
  res = map(lambda c: {"id": c["id"], "score": input.similarity(c['nlp']), "str": c['query']}, commandNodes)
  res = [r for r in res if r["score"] > 0.5]
  res = sorted(res, key=lambda r: r["score"], reverse=True)
  res = res[:10]
  return res

def compareWithHelp(inputStr):
  input = nlp(inputStr)
  res = map(lambda c: {"id": c["id"], "score": input.similarity(c['nlp']), "str": c['query']}, helpCommandNodes)
  res = [r for r in res if r["score"] > 0.5]
  res = sorted(res, key=lambda r: r["score"], reverse=True)
  res = res[:10]
  return res
