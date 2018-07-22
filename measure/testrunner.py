import csv, json, os
from typing import List

from datetime import datetime
from models import baselineModel_lg, baselineModel_sm
from modelBase import CliNlpModel, Suggestion
from testset import TestCase, TestSet, testset_queries

class TestCaseResult:
  def __init__(self, testCase: TestCase, matchedIndex: int = -1, matchedSuggestion: Suggestion = None):
    self.testCase = testCase
    self.matchedIndex = matchedIndex
    self.matchedSuggestion = matchedSuggestion

class TestRunner:
  def __init__(self, testSet: TestSet, cliModel: CliNlpModel):

    self._cliModel = cliModel
    self._testSet = testSet
    self._testCaseResults = None

  def getTestCaseResult(self, case: TestCase):
    suggestions = self._cliModel.getSuggestions(case.query, top = 100)

    for index in range(len(suggestions)):
      sug = suggestions[index]
      if case.match(sug.cliNode.id):
        return TestCaseResult(case, index, sug)
    
    return TestCaseResult(case)

  def getTestResults(self):
    if self._testCaseResults is None:
      self._testCaseResults = [self.getTestCaseResult(case) for case in self._testSet.testCases]

    return self._testCaseResults

  def run(self):
    if not os.path.isdir('measure/output'):
      os.makedirs('measure/output')

    results = self.getTestResults()
    filepath = self._getTestRunFilePath()

    TestRunner.writeToFile(filepath, results)
    print("Finished test run. Result saved to " + filepath)

  def _getTestRunFilePath(self):
    ts = datetime.now().strftime('%m%d%H%M%S')
    outputFilePath = 'measure/output/' + ts + '_' + self._testSet.id + '_' + self._cliModel.id + '.testrun.csv'
    
    return outputFilePath
  
  @staticmethod
  def writeToFile(outputFile: str, results: List[TestCaseResult]):
    with open(outputFile, 'w+', newline='') as csvfile:
      writer = csv.writer(csvfile)
     
      for res in results:
        if res.matchedIndex > -1:
          writer.writerow([
            res.testCase.query,
            res.matchedIndex,
            res.matchedSuggestion.score,
            res.matchedSuggestion.cliNode.id
          ])
        else:
          writer.writerow([
            res.testCase.query,
            -1,
            0,
            res.testCase.expectedCommands[0]
          ])
    
    baselineModel_sm

# runner = TestRunner(testset_queries, baselineModel_sm.load())
# runner.run()

runner = TestRunner(testset_queries, baselineModel_lg.load())
runner.run()

# TODO: add more runner to measure different combinations