import json, yaml, log
from typing import List
from datetime import datetime

from log import log
from utility.QueryRewriter import rewriteKnownTyposInQuery

import data

class Intent:
  def __init__(self, id, kind, quries):
    self.id = id
    self.kind = kind
    self.queries = quries

class IntentSet:
  def __init__(self, id, desc, createOn, intents: List[Intent]):
    self.id = id
    self.desc = desc
    self.createOn = createOn
    self.intents = [{"id": i.id, "kind": i.kind, "queries": i.queries} for i in intents]

  def getIntents(self):
    return [Intent(i["id"], i["kind"], i["queries"]) for i in self.intents]

def _getTs():
  ts = datetime.now().strftime('%m%d%H%M%S')
  return ts

def _loadFromYamlFile(filepath):
  obj = None
  with open(filepath, 'r') as stream:
    try:
       obj = yaml.load(stream)
    except yaml.YAMLError as exc:
      print(exc)
    except:
      print("error")

  return obj

def _saveToYamlFile(obj, filepath):
  with open(filepath, 'w') as outfile:
    yaml.dump(obj, outfile, default_flow_style=False)

  print("Saves to " + filepath)
  return filepath

def _getIdAsQuery(cliNode: data.CliNode) -> List[str]:
  return [cliNode.id]

def _getHelpAsQuery(cliNode: data.CliNode) -> List[str]:
  if cliNode.help is None:
    return [None]
  return [cliNode.help]

def _getIdAndHelp(cliNode: data.CliNode) -> List[str]:
  return map(rewriteKnownTyposInQuery, list(filter(None, _getIdAsQuery(cliNode) + _getHelpAsQuery(cliNode))))

def _getIntentSetFromClidata(id, desc= None, getQueries = None, cliData: data.CliData = None, top = None):
  if cliData is None:
    cliData = data.cliData

  if getQueries is None:
    getQueries = _getIdAndHelp

  nodes = cliData.getAllNodes()

  intents = []
  if top is None:
    top = len(nodes)

  for index in range(top):
    node = nodes[index]
    intents.append(Intent(node.id, node.cliType, list(getQueries(node))))

  ts = _getTs()
  return IntentSet(id, desc, ts, intents)

def getIntentSet():
  return _getIntentSetFromClidata("intent", cliData = data.cliData)

def getIntentSet_sm():
  return _getIntentSetFromClidata("intent_sm", cliData = data.cliData_sm)

def _updateIntentYamls():
  op = log().start("prepare data")
  intentSet = _getIntentSetFromClidata("cliIntent_default", "default cli intent data with id and help as trigger queries", _getIdAndHelp)
  op.end()

  op = log().start("save to file")
  _saveToYamlFile(intentSet, 'intent/cliIntent_default.yaml')
  op.end()

  intentSet_sm = _getIntentSetFromClidata("cliIntent_default_sm", "Small set of default cli intent data", _getIdAndHelp, top = 10)
  _saveToYamlFile(intentSet_sm, 'intent/cliIntent_sm.yaml')

  intentSet_idonly = _getIntentSetFromClidata("cliIntent_idonly", "Small set of default cli intent data", _getIdAsQuery)
  _saveToYamlFile(intentSet_idonly, 'intent/cliIntent_idonly.yaml')

# _updateIntentYamls()
