import data, spacy, time
import numpy as np
from typing import List

import en_core_web_lg as model_lg
import en_core_web_sm as model_sm

from log import log
from modelBase import CliNlpModel
from utility.QueryRewriter import rewriteAbbrInQuery, rewriteKnownTyposInQuery
from utility.AzureResourceRecognizer import AzureResourceRecognizer
from utility.UpdateDocVector import updateDocVector
from utility.SpellChecker import correctSpellingErrors

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
    return [None]
  return [cliNode.help]

def getIdAndHelp(cliNode: data.CliNode) -> List[str]:
  return map(rewriteKnownTyposInQuery, list(filter(None, getIdAsQuery(cliNode) + getHelpAsQuery(cliNode))))

def getAllAsQueries(cliNode: data.CliNode) -> List[str]:
  return map(rewriteKnownTyposInQuery, list(filter(None, getIdAsQuery(cliNode) + getHelpAsQuery(cliNode) + cliNode.queries)))

def getBaselineModel():
  nlp = model_lg.load()
  return CliNlpModel("lgd_lgm", getAllAsQueries, data.cliData, nlp)

def getBaselineModel_idonly():
  nlp = model_lg.load()
  return CliNlpModel("lgd_lgm_idonly", getIdAsQuery, data.cliData, nlp)

def getBaselineModel_sm():
  nlp = model_sm.load()
  return CliNlpModel("smd_smm", getAllAsQueries, data.cliData_sm, nlp)

def getBaselineModel_partial():
  nlp = model_lg.load()
  return CliNlpModel("pad_lgm", getAllAsQueries, data.cliData_partial, nlp)

def getModelWithAbbrQR_partial():
  nlp = model_lg.load()
  return CliNlpModel("pad_lgm_abbrqr", getAllAsQueries, data.cliData_partial, nlp, rewriteAbbrInQuery)

def getModelWithAbbrQR():
  nlp = model_lg.load()
  return CliNlpModel("lgd_lgm_abbrqr", getAllAsQueries, data.cliData, nlp, rewriteAbbrInQuery)

def getModelWithAbbrQRAndSpeller():
  nlp = model_lg.load()
  return CliNlpModel("lgd_lgm_abbrqr_speller", getAllAsQueries, data.cliData, nlp,
    rewriteDataQuery=rewriteAbbrInQuery,
    rewriteUserQuery=lambda q: correctSpellingErrors(rewriteAbbrInQuery(q)))

def getModelWithAzureResourceRecognizer():
  nlp = model_lg.load()
  azureResourceRecognizer = AzureResourceRecognizer(nlp)
  nlp.add_pipe(azureResourceRecognizer, last=True)
  return CliNlpModel("lgd_lgm_azRecognizer", getAllAsQueries, data.cliData, nlp, rewriteAbbrInQuery, updateDocVector)
