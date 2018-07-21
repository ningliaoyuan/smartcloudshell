from flask import Flask, jsonify
app = Flask(__name__)

print("initializing")

from models import baselineModel_lg
from modelBase import Suggestion

cliModel = baselineModel_lg.load()

@app.route('/')
def hello_world():
  return 'Welcome to smart cloud shell!'

@app.route('/cli/<string:query>')
def cliWithCmd(query):
  result = cliModel.getLagacyResult(query)
  return jsonify(result)

@app.route('/cli/help/<string:query>')
def cliWithHelp(query):
  result = cliModel.getLagacyResult(query)
  return jsonify(result)

print("localhost:5000 is serving")

if __name__ == '__main__':
  app.run(host='0.0.0.0')
