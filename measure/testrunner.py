import csv, json, os, yaml
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

class TestSummary:
  def __init__(self, ts: str, modelId: str, testSetId: str, total, precision, top3recall, top10recall):
    self.ts = ts
    self.modelId = modelId
    self.testSetId = testSetId
    self.total = total
    self.precision = precision
    self.top3recall = top3recall
    self.top10recall = top10recall
    self.id = self.ts + '_' + self.testSetId + '_' + self.modelId

class TestReport:
  def __init__(self, ts: str, modelId: str, testSetId: str, testCaseResults: List[TestCaseResult]):
    self.testCaseResults = testCaseResults

    total = len(self.testCaseResults)

    def filterByIndex(result: TestCaseResult, index: int) -> bool:
      return result.matchedIndex > -1 and result.matchedIndex <= index

    def cal(matchedResult: List[TestCaseResult], total: int) -> float:
      return round(len(matchedResult) / total, 4)

    top10Matched = list(filter(lambda r: filterByIndex(r, 10), self.testCaseResults))
    top10recall = cal(top10Matched, total)

    top3Matched = list(filter(lambda r: filterByIndex(r, 3), top10Matched))
    top3recall = cal(top3Matched, total)

    top1Matched = list(filter(lambda r: filterByIndex(r, 1), top3Matched))
    precision = cal(top1Matched, total)

    self.summary = TestSummary(ts, modelId, testSetId, total, precision, top3recall, top10recall)

  def saveToYamlFile(self, filepath = None):
    if filepath is None:
      filepath = 'measure/output/' + self.summary.id + '.report.yaml'

    with open(filepath, 'w') as outfile:
      yaml.dump(self, outfile, default_flow_style=False)

    print("Test report saves to " + filepath)

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

  def run(self) -> TestReport:
    if not os.path.isdir('measure/output'):
      os.makedirs('measure/output')

    results = self.getTestResults()

    ts = datetime.now().strftime('%m%d%H%M%S')
    report = TestReport(ts, self._cliModel.id, self._testSet.id, results)

    return report

# runner = TestRunner(testset_queries, baselineModel_sm.load())
# report = runner.run()
# report.saveToYamlFile()

runner = TestRunner(testset_queries, baselineModel_lg.load())
report = runner.run()
report.saveToYamlFile()

# TODO: add more runner to measure different combinations
