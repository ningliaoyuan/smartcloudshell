import csv, json, os
from typing import List
from log import log

import data
import testset

nodes = data.cliData.getAllNodes()

def saveToCsv(filepath: str, data: List[List]):
  with open(filepath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for index in range(len(data)):
      row = data[index]
      writer.writerow(row)

def getTestCaseCsvArrayFromNode(node: data.CliNode) -> List[str]:
  # Only take the 1st sentence
  if node.help is not None:
    help = node.help.split('.')[0]
    return testset.TestCase(help, node.id).getCsvArray()

  return None

data = list(filter(None, map(getTestCaseCsvArrayFromNode, nodes)))
filepath = 'measure/testset/helpToCommand.csv'
saveToCsv(filepath, data)

print("Generated test set: helpToCommand to ", filepath)