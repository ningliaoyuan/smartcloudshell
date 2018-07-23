import csv, json, os, yaml
from typing import List

from datetime import datetime
from modelBase import CliNlpModel, Suggestion
from measure.testset import TestCase, TestSet, testset_queries

class TestCaseResult:
  def __init__(self, testCase: TestCase, suggestions: List[Suggestion], matchedIndex: int = -1, matchedSuggestion: Suggestion = None):
    self.testCase = testCase
    self.matchedIndex = matchedIndex
    self.matchedSuggestion = matchedSuggestion
    self.suggestions = suggestions

class TestSummary:
  def __init__(self, ts: str, testSetId: str, modelId: str, total, precision, top3recall, top10recall):
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

    self.summary = TestSummary(ts, testSetId, modelId, total, precision, top3recall, top10recall)

  def saveToYamlFile(self, filepath = None):
    if filepath is None:
      filepath = 'measure/output/' + self.summary.id + '.report.yaml'

    with open(filepath, 'w') as outfile:
      yaml.dump(self, outfile, default_flow_style=False)

    print("Test report saves to " + filepath)
    return filepath

  @staticmethod
  def loadFromYamlFile(filename):
    filepath = 'measure/output/%s.yaml' % filename

    with open(filepath, 'r') as stream:
      try:
          testReport = yaml.load(stream)
      except yaml.YAMLError as exc:
          print(exc)

    return testReport

class CaseResultDiff:
  def __init__(self, testCase: TestCase, report1Suggestions: List[Suggestion], report2Suggestions: List[Suggestion], report1MatchedIndex: int, report2MatchedIndex: int):
    self.case = testCase
    self.report1Suggestions = report1Suggestions
    self.report2Suggestions = report2Suggestions
    self.report1MatchedIndex = report1MatchedIndex
    self.report2MatchedIndex = report2MatchedIndex

    if report1MatchedIndex == -1:
      report1MatchedIndex = 10000

    if report2MatchedIndex == -1:
      report1MatchedIndex = 10000

    if report1MatchedIndex < report2MatchedIndex:
      self.report1Score = 1
    elif report1MatchedIndex > report2MatchedIndex:
      self.report1Score = -1
    else:
      self.report1Score = 0

class TestReportDiff:
  def __init__(self, score, summary1: TestSummary, summary2: TestSummary, diffs: List[CaseResultDiff]):
    self.score = score
    self.summary1 = summary1
    self.summary2 = summary2
    self.z_diffs = diffs

  def saveToYamlFile(self, filepath = None):
    if filepath is None:
      filepath = 'measure/output/' + self.summary1.id + '_' + self.summary2.id + '.diff.yaml'

    with open(filepath, 'w') as outfile:
      yaml.dump(self, outfile, default_flow_style=False)

    print("Test report diff saves to " + filepath)
    return filepath

  @classmethod
  def diffReports(cls, report1: TestReport, report2: TestReport):
    if report1.summary.testSetId != report2.summary.testSetId:
      return None

    diffs = []
    score = 0
    for index in range(len(report1.testCaseResults)):
      res1 = report1.testCaseResults[index]
      res2 = report2.testCaseResults[index]

      if(res1.matchedIndex == res2.matchedIndex):
        continue

      diff = CaseResultDiff(res1.testCase, res1.suggestions, res2.suggestions, res1.matchedIndex, res2.matchedIndex)
      score += diff.report1Score

      diffs.append(diff)

    return cls(score, report1.summary, report2.summary, diffs)

  @staticmethod
  def loadFromYamlFile(filename):
    filepath = 'measure/output/%s.yaml' % filename

    with open(filepath, 'r') as stream:
      try:
          testReportDiff = yaml.load(stream)
      except yaml.YAMLError as exc:
          print(exc)

    return testReportDiff

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
        return TestCaseResult(case, suggestions[:3], index, sug)

    return TestCaseResult(case, suggestions[:3])

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
