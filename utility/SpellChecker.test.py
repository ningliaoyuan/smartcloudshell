from pprint import pprint
from SpellChecker import correctSpellingErrors

def executeTestCase(testCases, queryRewriteFn):
    for testCase in testCases:
        output = queryRewriteFn(testCase[0])
        assert (output == testCase[1]), output + " != " + testCase[1]

testCases = [
    ["starrt my vm.", "start my vm."],
    ["How to craete vmss?", "How to create vmss?"],
    ["steps to creat sf and vm", "steps to create sf and vm"]
]
executeTestCase(testCases, correctSpellingErrors)

print("completed")