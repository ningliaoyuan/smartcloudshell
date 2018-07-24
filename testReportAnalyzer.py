import sys, csv
args = sys.argv
from measure.testrunner import TestReportDiff

fileName = 'queries_lgd_lgm_abbr_VS_queries_lgd_lgm.diff'
diff = TestReportDiff.loadFromYamlFile(fileName)

outputFile = 'measure/output/' + fileName + '.csv'
with open(outputFile, 'w+', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow([
      'Query',
      'Expected command(s)',
      'Report 1 Score',
      'Report 1 Matched Index',
      'Report 1 Suggestions',
      'Report 2 Matched Index',
      'Report 2 Suggestions'
  ])
  for row in diff.z_diffs:
      writer.writerow([
          row.case.query,
          ', '.join(row.case.expectedCommands),
          row.report1Score,
          row.report1MatchedIndex,
          ', '.join(map(lambda s: s.cliNode.id, row.report1Suggestions)),
          row.report2MatchedIndex,
          ', '.join(map(lambda s: s.cliNode.id, row.report1Suggestions))
      ])

print('done')