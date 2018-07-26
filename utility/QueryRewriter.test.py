from pprint import pprint
from QueryRewriter import rewriteAbbrInQuery, rewriteKnownTyposInQuery, rewriteStopWords, combineQueryRewriters

def executeTestCase(testCases, queryRewriteFn):
    for testCase in testCases:
        output = queryRewriteFn(testCase[0])["query"]
        assert (output == testCase[1]), output + " != " + testCase[1]

abbrTestCases = [
    ["start my vm.", "start my virtual machine."],
    ["How to create vmss?", "How to create virtual machine scale set?"],
    ["steps to create sf and vm", "steps to create service fabric and virtual machine"],
    ["Set sp", "Set service principal"],
    ["vm1vm1vm1 vm, ??vmss v2m v m", "vm1vm1vm1 virtual machine, ??virtual machine scale set v2m v m"],
]
executeTestCase(abbrTestCases, rewriteAbbrInQuery)

def executeTestCase2(testCases, queryRewriteFn):
  for testCase in testCases:
    output= queryRewriteFn(testCase[0])
    assert (output == testCase[1]), output + " != " + testCase[1]

knownTypoTestCases = [
    ["Detatch a managed disk from a VM.", "detach a managed disk from a VM."],
    ["List unamanaged disks of a VM.", "List unmanaged disks of a VM."]
]
executeTestCase2(knownTypoTestCases, rewriteKnownTyposInQuery)

executeTestCase([
    ["Delete a azure vm", "Delete vm"],
    ["Create a new website", "Create website"],
    ["Steps to start my my my website", "Steps start website"],
    ["my website stop", "website stop"]
], rewriteStopWords)

rewriteAll = combineQueryRewriters([rewriteAbbrInQuery, rewriteStopWords])
executeTestCase([
    ["Delete a azure vm", "Delete virtual machine"],
    ["Create a new website", "Create web app"],
    ["Steps to start my my my website", "Steps start web app"],
    ["my website stop", "web app stop"]
], rewriteAll)

pprint("completed")
