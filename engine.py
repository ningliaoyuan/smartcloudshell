import modelFactory
from modelBase import Suggestion
from typing import List
from log import log

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
    op.end("Done")

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
      searchResults = []
    else:
      searchResults = [] # TBD: haitao

    return _composeResult(cliSuggestions, customResponse, searchResults)