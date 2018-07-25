from enum import Enum
from log import log
from data import CliNode, CliData
from random import randint

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

  def getCustomResponse(self, query) -> str:
    customDict = {
      "hi": ["you should say hey"],
      "bye": ["see you later"],
      "what can you do":
        [
          "I can do anything. please give me a vote"
        ],
      "tell me a joke":
        [
          "My wife accused me of being immature, I told her to get out of my fort.",
          "Someone stole my mood ring, I don’t know how I feel about that.",
          "I broke my finger last week, on the other hand, I am okay.",
          "Someone stole my Microsoft office and they’re gonna pay, you have my word.",
          "What do you call a dog with no legs, it doesn’t matter, it’s not going to come anyway."
        ]
    }

    res = customDict.get(query, None)
    index = randint(0, len(res) - 1)

    return res[index]
