from enum import Enum
from log import log
from data import CliNode, CliData

# suggetion result
class Suggestion:
  def __init__(self, cliNode: CliNode, score):
    self.cliNode = cliNode
    self.score = score
  
  def mapSuggestionToRes(self):
    return {
      "id": self.cliNode.id,
      "score": self.score,
      "str": self.cliNode.help
    }

  def __str__(self):
    return (self.cliNode.id, self.cliNode.help, self.score).__str__()

  def __repr__(self):
    return (self.cliNode.__repr__(), self.score).__str__()

def mapSuggestionToRes(suggestion: Suggestion):
  return suggestion.mapSuggestionToRes()

# Nlp Processed Cli Node
class NlpCliNode:
  def __init__(self, cliNode, nlpQueries):
    self.cliNode = cliNode
    self.nlpQueries = nlpQueries

  def compare(self, nlpQuery):
    scores = map(nlpQuery.similarity, self.nlpQueries)
    return max(scores)

class CliNlpModel:
  def __init__(self, cliData: CliData, nlpModel, rewriteQuery = None, scoreThreshold = 0.5):
    self._cliData = cliData
    self._nlp = nlpModel
    self.scoreThreshold = scoreThreshold

    if rewriteQuery is not None:
      self.rewriteQuery = rewriteQuery      
    else:
      self.rewriteQuery = lambda query: query

    self.nlpNodes = list(map(self._getNlpCliNode, cliData.getAllNodes()))

  def _getNlpQuery(self, query):
    rewrittenQuery = self.rewriteQuery(query)
    nlpQuery = self._nlp(rewrittenQuery)
    return nlpQuery

  def _getNlpCliNode(self, cliNode: CliNode) -> NlpCliNode:
    queries = cliNode.getQueries()
    nlpQueries = list(map(self._getNlpQuery, queries))
    return NlpCliNode(cliNode, nlpQueries)

  def getSuggestions(self, queryStr, top = 100):
    nlpQuery = self._getNlpQuery(queryStr)
    scoredNodes = map(lambda nlpCliNode: Suggestion(nlpCliNode.cliNode, nlpCliNode.compare(nlpQuery)), self.nlpNodes)
    matches = filter(lambda scoredNode: scoredNode.score > self.scoreThreshold, scoredNodes)
    sortedMatches = sorted(matches, key=lambda suggestion: suggestion.score, reverse=True)
    return sortedMatches[:100]

  def getLagacyResult(self, queryStr, top = 10):
    suggestions = self.getSuggestions(queryStr, top)
    result = list(map(mapSuggestionToRes, suggestions))
    return result