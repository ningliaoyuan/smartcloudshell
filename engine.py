import sys, modelFactory
from typing import List
from log import log
from aladdinSearch import AladdinSearch
from datetime import datetime
from modelBase import Suggestion
from data import cliData

def _composeResult(suggestions: List, cliCorrections: dict, customResponses: List, searchResults: List):
    return {
      "cli": suggestions,
      "cliCorrections": cliCorrections,
      "custom": customResponses,
      "search": searchResults
    }

def _getCliNodeById(id):
  return cliData.getCliNodeById(id)

class Engine:
  def __init__(self, isDev = False):
    op = log().start("Initializing model and index")
    if isDev:
      self.intentModel = modelFactory.getModelWithAbbrQRAndSpeller_smdata_smmodel()
    else:
      self.intentModel = modelFactory.getBaselineModel()
    op.end("Done")

    self.aladdin = AladdinSearch()

    self.diag = {
      "modelid": self.intentModel.id
    }
    if isDev:
      self.diag["isDev"] = True

  def getResponse(self, query, enableSearch, enableCustomResponse, top = 10):
    if enableCustomResponse:
      customResponse = self.intentModel.getCustomResponse(query)
    else:
      customResponse = None

    promise = None
    if enableSearch:
      promise = self.aladdin.search(query)

    cliCorrections, cliSuggestions = [], []

    if customResponse is None or len(customResponse) == 0:
      intentSuggestions, cliCorrections = self.intentModel.getMatchedIntents(query, top)

      for intentSug in intentSuggestions:
        cliNode = _getCliNodeById(intentSug.intent.id)
        cliSuggestions.append({
          "id": cliNode.id,
          "help": cliNode.help,
          "cliType": cliNode.cliType,
          "score": intentSug.score,
          "executable": False, # TBD
          "parameters": [] # TBD
        })

    searchResults = []
    if promise is not None:
      try:
        searchResults = self.aladdin.resolveRequest(promise)
      except TimeoutError:
        print("Timed out when calling search")
      except:
        print("Unexpected error when calling search:", sys.exc_info()[0])

    return _composeResult(cliSuggestions, cliCorrections, customResponse, searchResults)

if __name__ == '__main__':
  engine = Engine()
  response = engine.getResponse('Creat storage accont', False, True)
  import json
  print(json.dumps(response))