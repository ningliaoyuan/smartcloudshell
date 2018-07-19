import json

#with open ('./data/help_dump_small.json') as f:
with open ('./data/help_dump.json') as f:
  data = json.load(f)


def getCommandWithCommand(jsonNode):
    command =  jsonNode[0]
    return {
        "id": command,
        "query": command,
    }

def getCommandWithHelp(jsonNode):
    command =  jsonNode[0]
    help = jsonNode[1]["help"]
    if help is None:
        help = ""
    return {
        "id": command,
        "query": help
    }


def getAllCommandsWithHelpAsQuery():
    commandHelpQueries = map(getCommandWithHelp, data.items())
    commandHelpQueriesWithoutEmptyHelp = filter(lambda q: len(q["query"]) > 0, commandHelpQueries)
    return list(commandHelpQueriesWithoutEmptyHelp)

def getAllCommandsWithCommandAsQuery():
    commandHelpQueries = map(getCommandWithCommand, data.items())
    return list(commandHelpQueries)


# print(getAllCommandsWithHelpAsQuery())
