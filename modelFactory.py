
import data, spacy, time
import numpy as np
from typing import List

import en_core_web_lg as model_lg
import en_core_web_sm as model_sm

from log import log
from modelBase import CliNlpModel

def getVector(vocab, words):
  tokens = words.split(' ')
  vectors = list(map(vocab.get_vector, tokens))
  return np.mean(vectors, axis = 0)

def addAbbrVector(nlp):
    vocab = nlp.vocab
    abbrDic = data.loadAbbrDic()

    for abbr, phrase in abbrDic.items():
      try:
        # vector = nlp(phrase).vector
        vector = getVector(vocab, phrase)
        vocab.set_vector(abbr, vector)
      except:
        print("Unexpected error:", abbr, phrase)
      else:
        print("done", abbr)

    return nlp

def getIdAsQuery(cliNode: data.CliNode) -> List[str]:
  return [cliNode.id]

def getHelpAsQuery(cliNode: data.CliNode) -> List[str]:
  if cliNode.help is None:
    return None
  return [cliNode.help]

def getIdAndHelp(cliNode: data.CliNode) -> List[str]:
  return list(filter(None, getIdAsQuery(cliNode) + getHelpAsQuery(cliNode)))

def getAllAsQuries(cliNode: data.CliNode) -> List[str]:
  return list(filter(None, getIdAsQuery(cliNode) + getHelpAsQuery(cliNode) + cliNode.queries))

def getBaselineModel():
  nlp = model_lg.load()
  return CliNlpModel("lgd_lgm", getAllAsQuries, data.cliData, nlp)

def getBaselineModel_sm():
  nlp = model_sm.load()
  return CliNlpModel("smd_smm", getAllAsQuries, data.cliData_sm, nlp)

def getBaselineModel_partial():
  nlp = model_lg.load()
  return CliNlpModel("pad_lgm", getAllAsQuries, data.cliData_partial, nlp)

def getModelWithAbbrVectorAssigned():
  nlp = model_lg.load()
  nlp = addAbbrVector(nlp)
  return CliNlpModel("lgd_lgm_abbr", getAllAsQuries, data.cliData, nlp)
