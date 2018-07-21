import spacy

from models import baselineModel_lg

cliModel = baselineModel_lg.load()

def compare(inputStr):
  res = cliModel.getLegacyResult(inputStr)
  return res

def compareWithHelp(inputStr):
  res = cliModel.getLegacyResult(inputStr)
  return res
