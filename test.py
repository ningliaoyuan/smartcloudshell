import csv, json, os
from datetime import datetime
from nlp import compare, compareWithHelp

class TestCase:

  def __init__(self, query, expectedCommand):
    self.query = query
    self.expectedCommands = expectedCommand.split('|')
    self.matchWithCmd = ''
    self.scoreWithCmd = 0
    self.isMatchCmdCorrect = None
    self.matchWithHelp = ''
    self.scoreWithHelp = 0
    self.isMatchHelpCorrect = None

  def runTest(self):

    r1 = compare(self.query)
    if len(r1) >= 1:
      self.matchWithCmd = r1[0]['id']
      self.scoreWithCmd = r1[0]['score']
      self.isMatchCmdCorrect = self.matchWithCmd in self.expectedCommands

    r2 = compareWithHelp(self.query)
    if len(r2) >= 1:
      self.matchWithHelp = r2[0]['id']
      self.scoreWithHelp = r2[0]['score']
      self.isMatchHelpCorrect = self.matchWithHelp in self.expectedCommands

  def __str__(self):
    return (
      self.query,
      self.expectedCommands,
      self.matchWithCmd,
      self.scoreWithCmd,
      self.isMatchCmdCorrect,
      self.matchWithHelp,
      self.scoreWithHelp,
      self.isMatchHelpCorrect
    ).__str__()

  def __repr__(self):
    return self.__str__()

cases = []

with open('testset/queries.csv') as csvfile:
  queries = csv.reader(csvfile)
  for row in queries:
    if len(row) == 0:
      continue
    cases.append(TestCase(row[0], row[1]))

for c in cases:
  c.runTest()

ts = datetime.now().strftime('%H%M%S')
outputFile = 'output/testrun-' + ts + '.csv'
if not os.path.isdir('output'):
  os.makedirs('output')

with open(outputFile, 'w+') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow([
    'Query',
    'Expected command',
    'Prediction1',
    'Score1',
    'Prediction1 correct',
    'Prediction2',
    'Score2',
    'Prediction2 correct'
  ])
  for c in cases:
    writer.writerow([
      c.query,
      ', '.join(c.expectedCommands),
      c.matchWithCmd,
      c.scoreWithCmd,
      c.isMatchCmdCorrect,
      c.matchWithHelp,
      c.scoreWithHelp,
      c.isMatchHelpCorrect
    ])

print('Test result saved to ' + outputFile)
