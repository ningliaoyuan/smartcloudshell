import json


# all cli obj

def createCliNodeFromJsonNode(jsonNode):
  command = jsonNode[0]
  help = jsonNode[1]["help"]
  params = jsonNode[1].get("parameters", None)

  if params is not None:
    cliType = "command"
  else:
    cliType = "group"

  return CliNode(command, help, cliType)


class CliNode:
  def __init__(self, id, help, cliType):
    self.id = id
    self.help = help
    self.cliType = cliType
  def getQueries(self):
    # filter out empty or null string
    return filter(None, [self.id, self.help])
  
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
