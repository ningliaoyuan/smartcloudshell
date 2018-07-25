import sys, modelFactory
from typing import List
from log import log
from aladdinSearch import AladdinSearch
from datetime import datetime

def _composeResult(cliSuggestions: List, cliCorrections: dict, customResponses: List, searchResults: List):
    return {
      "cli": cliSuggestions,
      "cliCorrections": cliCorrections,
      "custom": customResponses,
      "search": searchResults
    }

class Engine:
  def __init__(self, isDev = False):
    op = log().start("Initializing model and index")
    if isDev:
      self.cliModel = modelFactory.getModelWithAbbrQRAndSpeller_smdata_smmodel()
    else:
      self.cliModel = modelFactory.getBaselineModel()
    op.end("Done")

    self.aladdin = AladdinSearch()

  def getLegacyResult(self, query):
    return self.cliModel.getLegacyResult(query)

  def getResponse(self, query, enableSearch, enableCustomResponse):
    if enableCustomResponse:
      customResponse = self.cliModel.getCustomResponse(query)
    else:
      customResponse = None

    promise = None
    if enableSearch:
      promise = self.aladdin.search(query)

    if customResponse is None or len(customResponse) == 0:
      cliSuggestions, cliCorrections = self.cliModel.getLegacyResult(query)
    else:
      cliSuggestions = []

    searchResults = []
    if promise is not None:
      try:
        searchResults = self.aladdin.resolveRequest(promise)
      except TimeoutError:
        print("Timed out when calling search")
      except:
        print("Unexpected error when calling search:", sys.exc_info()[0])
    else:
      searchResults = []

    return _composeResult(cliSuggestions, cliCorrections, customResponse, searchResults)

if __name__ == '__main__':
  engine = Engine()
  response = engine.getResponse('Creat storage accont', False, True)
  import json
  print(json.dumps(response))