import modelFactory
from modelBase import Suggestion
from typing import List
from log import log
from aladdinSearch import AladdinSearch
from datetime import datetime

def _composeResult(cliSuggestions: List, customResponses: List, searchResults: List):
    return {
      "cli": cliSuggestions,
      "custom": customResponses,
      "search": searchResults
    }

class Engine:
  def __init__(self):
    op = log().start("Initializing model and index")
    self.cliModel = modelFactory.getBaselineModel()
    f = open(datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S'), 'wb')
    f.close()
    op.end("Done")

    self.aladdin = AladdinSearch()

  def getLegacyResult(self, query):
    return self.cliModel.getLegacyResult(query)

  def getResponse(self, query, enableSearch, enableCustomResponse):
    if enableCustomResponse:
      customResponse = self.cliModel.getCustomResponse(query)
    else:
      customResponse = None

    if customResponse is None or len(customResponse) == 0:
      cliSuggestions = self.cliModel.getLegacyResult(query)
    else:
      cliSuggestions = []

    if enableSearch:
      promise = self.aladdin.search(query)
      searchResults = self.aladdin.resolveRequest(promise)
    else:
      searchResults = [] # TBD: haitao

    return _composeResult(cliSuggestions, customResponse, searchResults)
