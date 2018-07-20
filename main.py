from flask import Flask, jsonify
app = Flask(__name__)

print("initializing")

from models import baselineModel_lg
from modelBase import Suggestion

cliModel = baselineModel_lg.load()


def mapSuggestionToRes(suggestion: Suggestion):
  return {
    "id": suggestion.cliNode.id,
    "score": suggestion.score,
    "str": suggestion.cliNode.help
  }

@app.route('/')
def hello_world():
  return 'Welcome to smart cloud shell!'

@app.route('/cli/<string:query>')
def cliWithCmd(query):
  suggestions = cliModel.getSuggestions(query)
  result = list(map(mapSuggestionToRes, suggestions))
  
  return jsonify(result)

@app.route('/cli/help/<string:query>')
def cliWithHelp(query):
  suggestions = cliModel.getSuggestions(query)
  result = list(map(mapSuggestionToRes, suggestions))
  return jsonify(result)

print("localhost:5000 is serving")

if __name__ == '__main__':
  app.run()
