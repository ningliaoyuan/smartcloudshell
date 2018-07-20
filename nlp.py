import spacy

from models import baselineModel_lg
from modelBase import Suggestion

cliModel = baselineModel_lg.load()

def compare(inputStr):
  res = cliModel.getLagacyResult(inputStr)
  return res

def compareWithHelp(inputStr):
  res = cliModel.getLagacyResult(inputStr)
  return res
