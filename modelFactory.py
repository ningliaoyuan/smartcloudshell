import data, spacy, time
import numpy as np
from typing import List

import en_core_web_lg as model_lg
import en_core_web_sm as model_sm

from log import log
from modelBase import CliNlpModel
from utility.QueryRewriter import rewriteAbbrInQuery, combineQueryRewriters
from utility.AzureResourceRecognizer import AzureResourceRecognizer
from utility.UpdateDocVector import updateDocVector
from utility.SpellChecker import correctSpellingErrors
from intentData import getIntentSet, getIntentSet_sm

def getBaselineModel():
  return getModelWithAbbrQRAndSpeller()

def getModelWithAbbrQR():
  nlp = model_lg.load()
  return CliNlpModel("lgd_lgm_abbrqr", getIntentSet(), nlp, rewriteAbbrInQuery)

def getModelWithAbbrQRAndSpeller():
  nlp = model_lg.load()
  return CliNlpModel("lgd_lgm_abbrqr_speller", getIntentSet(), nlp,
    rewriteDataQuery=rewriteAbbrInQuery,
    rewriteUserQuery=combineQueryRewriters(rewriteAbbrInQuery, correctSpellingErrors))

def getModelWithAbbrQRAndSpeller_smdata_smmodel():
  nlp = model_sm.load()
  return CliNlpModel("smdata_smmodel_abbrqr_speller", getIntentSet_sm(), nlp,
    rewriteDataQuery=rewriteAbbrInQuery,
    rewriteUserQuery=combineQueryRewriters(rewriteAbbrInQuery, correctSpellingErrors))

def getModelWithAzureResourceRecognizer():
  nlp = model_lg.load()
  intentSet = getIntentSet()
  azureResourceRecognizer = AzureResourceRecognizer(nlp)
  nlp.add_pipe(azureResourceRecognizer, last=True)
  return CliNlpModel("lgd_lgm_azRecognizer", intentSet, nlp, rewriteAbbrInQuery, preProcessDoc = updateDocVector)
