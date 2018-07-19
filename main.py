from flask import Flask, jsonify
app = Flask(__name__)

print("initializing")

from nlp import compare, compareWithHelp

@app.route('/')
def hello_world():
  return 'Welcome to smart cloud shell!'

@app.route('/cli/<string:query>')
def cliWithCmd(query):
  result = compare(query)
  return jsonify(result)

@app.route('/cli/help/<string:query>')
def cliWithHelp(query):
  result = compareWithHelp(query)
  result = result + compare(query)
  result = sorted(result, key=lambda r: r["score"], reverse=True)
  return jsonify(result)

print("localhost:5000 is serving")

if __name__ == '__main__':
  app.run()
