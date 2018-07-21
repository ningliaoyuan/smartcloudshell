import json
from typing import List


def createCliNodeFromJsonNode(jsonNode):
  command = jsonNode[0]
  help = jsonNode[1]["help"]
  params = jsonNode[1].get("parameters", None)

  if params is not None:
    cliType = "command"
  else:
    cliType = "group"

  # create initial queries
  queries = list(filter(None, [command, help]))

  return CliNode(command, help, cliType, queries)

class CliNode:
  def __init__(self, id, help, cliType, queries: List[str]):
    self.id = id
    self.help = help
    self.cliType = cliType
    self.queries = queries

  def getQueries(self) -> List[str]:
    return self.queries
    
  def __str__(self):
    return (self.id, self.cliType, self.help).__str__()

  def __repr__(self):
    return self.__str__()

class CliData:
  def __init__(self, dataJson):
    self._dataJson = dataJson
    self._nodes = list(map(createCliNodeFromJsonNode, self._dataJson .items()))
    self._commandNodes = list(filter(lambda n: n.cliType == "command", self._nodes))
  
  def getAllNodes(self):
    return self._nodes

  def getCommandNodes(self):
    return self._commandNodes

#with open ('./data/help_dump_small.json') as f:
with open ('./data/help_dump.json') as f:
  data = json.load(f)

cliData = CliData(data)

with open ('./data/help_dump_small.json') as f:
  data_sm = json.load(f)

cliData_sm = CliData(data_sm)
