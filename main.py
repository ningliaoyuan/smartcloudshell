from flask import Flask, jsonify, request
from log import log

from engine import Engine

app = Flask(__name__)

engine = Engine()

@app.route('/')
def hello_world():
  return 'Welcome to smart cloud shell! Please help with testing/labeling at https://bizqnabootcamp.azurewebsites.net/'

@app.route('/cli/<string:query>')
def cliWithCmd(query):
  result = engine.getLegacyResult(query)
  return jsonify(result)

@app.route('/cli/help/<string:query>')
def cliWithHelp(query):
  result = engine.getLegacyResult(query)
  return jsonify(result)

@app.route('/q/<string:query>')
def getResponse(query):
  search = request.args.get('s')
  if search is None or search == 'true':
    enableSearch = True

  custom = request.args.get('c')
  if custom is None or search == 'true':
    enableCustomResponse = True

  result = engine.getResponse(
    query,
    enableSearch = enableSearch,
    enableCustomResponse = enableCustomResponse)

  return jsonify(result)

port = 80
print("localhost:%d is serving" % port)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port)
