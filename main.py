from flask import Flask, jsonify
app = Flask(__name__)

print("initializing")

import modelFactory
from modelBase import Suggestion

cliModel = modelFactory.getBaselineModel()

@app.route('/')
def hello_world():
  return 'Welcome to smart cloud shell! Please help with testing/labeling at https://bizqnabootcamp.azurewebsites.net/'

@app.route('/cli/<string:query>')
def cliWithCmd(query):
  result = cliModel.getLegacyResult(query)
  return jsonify(result)

@app.route('/cli/help/<string:query>')
def cliWithHelp(query):
  result = cliModel.getLegacyResult(query)
  return jsonify(result)

port = 80
print("localhost:%d is serving" % port)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port)
