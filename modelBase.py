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
    maxScore = max(scores)
    return round(float(maxScore), 4)

class CliNlpModel:
  def __init__(self, id: str, getQueriesFromCliNode, cliData: CliData, nlpModel, rewriteDataQuery = None, preProcessDoc = None, scoreThreshold = 0.5, rewriteUserQuery = None):
    self.id = id
    self._cliData = cliData
    self._nlp = nlpModel
    self.scoreThreshold = scoreThreshold
    self._getQueriesFromCliNode = getQueriesFromCliNode

    if rewriteDataQuery is not None:
      self.rewriteDataQuery = rewriteDataQuery
    else:
      self.rewriteDataQuery = lambda query: query

    if rewriteUserQuery is not None:
      self.rewriteUserQuery = rewriteUserQuery
    else:
      self.rewriteUserQuery = self.rewriteDataQuery

    self.preProcessDoc = preProcessDoc

    op = log().start("processing data with model: " + self.id)
    self.nlpNodes = list(map(self._getNlpCliNode, cliData.getAllNodes()))
    op.end("done")

  def _getNlpQuery(self, query, queryRewriteFn):
    rewrittenQuery = queryRewriteFn(query)
    nlpQuery = self._nlp(rewrittenQuery)
    return nlpQuery

  def _getNlpQueryForData(self, query):
    return self._getNlpQuery(query, self.rewriteDataQuery)

  def _getNlpQueryForUserQuery(self, query):
    return self._getNlpQuery(query, self.rewriteUserQuery)

  def _getNlpCliNode(self, cliNode: CliNode) -> NlpCliNode:
    queries = self._getQueriesFromCliNode(cliNode)
    nlpQueries = list(map(self._getNlpQueryForData, queries))
    if self.preProcessDoc is not None:
      for nlpQuery in nlpQueries:
        self.preProcessDoc(nlpQuery)

    return NlpCliNode(cliNode, nlpQueries)

  def getSuggestions(self, queryStr, top = 100):
    nlpQuery = self._getNlpQueryForUserQuery(queryStr)
    if self.preProcessDoc is not None:
        self.preProcessDoc(nlpQuery)

    scoredNodes = list(map(lambda nlpCliNode: Suggestion(nlpCliNode.cliNode, nlpCliNode.compare(nlpQuery)), self.nlpNodes))
    matches = filter(lambda scoredNode: scoredNode.score > self.scoreThreshold, scoredNodes)
    sortedMatches = sorted(matches, key=lambda suggestion: suggestion.score, reverse=True)
    return sortedMatches[:top]

  def getLegacyResult(self, queryStr, top = 10):
    suggestions = self.getSuggestions(queryStr, top)
    result = list(map(mapSuggestionToRes, suggestions))
    return result
