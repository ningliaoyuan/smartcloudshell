import csv, json, os
from typing import List
from log import log

class TestCase:
  def __init__(self, query, expectedCommand):
    self.query = query
    self.expectedCommands = expectedCommand.split('|')

  def match(self, command: str) -> bool:
    return command in self.expectedCommands

  def getCsvArray(self) -> List:
    return [self.query, '|'.join(self.expectedCommands)]

class TestSet:
  def __init__(self, id: str, testCases: List[TestCase]):
    self.id = id
    self.testCases = testCases
    self.count = len(testCases)

  @classmethod
  def loadFromTestsFile(cls,  fileName: str, id: str = None):
    '''
    Load Test Set from file
    :param id: id of given test set
    :param fileName: the file name in file path: i.e.: 'measure/testset/{fileName}.csv'
    '''
    filePath = "measure/testset/%s.csv" % fileName

    op = log().start("Loading test set from: " + fileName)
    with open(filePath) as csvfile:
      queries = csv.reader(csvfile)
      testCases = [TestCase(query[0], query[1]) for query in filter(len, queries)]

    if id is None:
      id = fileName

    testSet = cls(id=id, testCases= testCases)
    op.end("%d test cases have been loaded." % testSet.count)

    return testSet

# export:
testset_queries = TestSet.loadFromTestsFile(fileName = 'queries')
testset_helptocommand = TestSet.loadFromTestsFile(fileName = 'helpToCommand')
testset_labeledqueries = TestSet.loadFromTestsFile(fileName = 'labeled_queries')

# print(testset_queries.count)
