from enum import Enum
from log import log
from data import CliNode, CliData
from random import randint
from intentData import Intent, IntentSet

# suggetion result
class Suggestion:
  def __init__(self, intent: Intent, score):
    self.intent = intent
    self.score = score

  def mapSuggestionToRes(self):
    return {
      "id": self.intent.id,
      "score": self.score,
      "str": self.intent.id
    }

class NlpIntent:
  def __init__(self, intent: Intent, nlpQueries):
    self.intent = intent
    self.nlpQueries = nlpQueries

  def compare(self, nlpQuery):
    scores = map(nlpQuery.similarity, self.nlpQueries)
    maxScore = max(scores)
    return round(float(maxScore), 4)

# TODO: rename to intentNlpModel
class CliNlpModel:
  def __init__(self, id: str, intentSet: IntentSet, nlpModel, rewriteDataQuery = None, preProcessDoc = None, scoreThreshold = 0.5, rewriteUserQuery = None):
    self.id = id
    self._nlp = nlpModel
    self.scoreThreshold = scoreThreshold

    if rewriteDataQuery is not None:
      self.rewriteDataQuery = rewriteDataQuery
    else:
      self.rewriteDataQuery = lambda query: { 'query': query, 'corrections': {} }

    if rewriteUserQuery is not None:
      self.rewriteUserQuery = rewriteUserQuery
    else:
      self.rewriteUserQuery = self.rewriteDataQuery

    self.preProcessDoc = preProcessDoc

    op = log().start("processing data with model: " + self.id)
    self.nlpIntents = list(map(self._getNlpIntent, intentSet.getIntents()))
    op.end("done")

  def _getNlpQuery(self, query, queryRewriteFn):
    rewrittenQuery = queryRewriteFn(query)
    nlpQuery = self._nlp(rewrittenQuery['query'])
    return nlpQuery, rewrittenQuery['corrections']

  def _getNlpQueryForData(self, query):
    return self._getNlpQuery(query, self.rewriteDataQuery)[0]

  def _getNlpQueryForUserQuery(self, query):
    return self._getNlpQuery(query, self.rewriteUserQuery)

  def _getNlpIntent(self, intent: Intent) -> NlpIntent:
    queries = intent.queries
    nlpQueries = list(map(self._getNlpQueryForData, queries))

    if self.preProcessDoc is not None:
      for nlpQuery in nlpQueries:
        self.preProcessDoc(nlpQuery)

    return NlpIntent(intent, nlpQueries)

  def getMatchedIntents(self, queryStr, top = 100):
    nlpQuery, corrections = self._getNlpQueryForUserQuery(queryStr)

    if self.preProcessDoc is not None:
        self.preProcessDoc(nlpQuery)

    scoredIntents = list(map(lambda nlpIntent: Suggestion(nlpIntent.intent, nlpIntent.compare(nlpQuery)), self.nlpIntents))
    matches = filter(lambda scoredNode: scoredNode.score > self.scoreThreshold, scoredIntents)
    sortedMatches = sorted(matches, key=lambda suggestion: suggestion.score, reverse=True)
    return sortedMatches[:top], corrections

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
    if res is None:
      return ""

    index = randint(0, len(res) - 1)

    return res[index]
