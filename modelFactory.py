import spacy, time
from log import log
from data import cliData, cliData_partial, cliData_sm
from modelBase import CliNlpModel

import en_core_web_lg as model_lg
import en_core_web_sm as model_sm

def getBaselineModel():
  nlp = model_lg.load()
  return CliNlpModel("lgd_lgm", cliData, nlp)

def getBaselineModel_sm():
  nlp = model_sm.load()
  return CliNlpModel("smd_smm", cliData_sm, nlp)

def getBaselineModel_partial():
  nlp = model_lg.load()
  return CliNlpModel("pad_lgm", cliData_partial, nlp)

def getModelWithAbbrVectorAssigned():
  nlp = model_lg.load()
  # TODO:
  return CliNlpModel("smd_smm", cliData_sm, nlp)
