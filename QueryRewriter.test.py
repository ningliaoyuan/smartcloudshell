from pprint import pprint
from QueryRewriter import rewriteQuery

testCases = [
    ["start my vm.", "start my virtual machine."],
    ["How to create vmss?", "How to create virtual machine scale set?"],
    ["steps to create sf and vm", "steps to create service fabric and virtual machine"],
    ["Set sp", "Set service principal"],
    ["vm1vm1vm1 vm, ??vmss v2m v m", "vm1vm1vm1 virtual machine, ??virtual machine scale set v2m v m"],
]

for testCase in testCases:
    output = rewriteQuery(testCase[0])
    assert (output == testCase[1]), output + " != " + testCase[1]

pprint("completed")