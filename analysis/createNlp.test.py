from createNlp import createNlp

nlp = createNlp()
testcases = [
    u"create vm",
    u"create virtual machine",
    u"create dla",
    u"create data lake analytics",
    u"delete sf",
]

for testcase1 in testcases:
    for testcase2 in testcases:
        if(testcase1 != testcase2):
            doc1 = nlp(testcase1)
            doc2 = nlp(testcase2)
            similarity = doc1.similarity(doc2)
            print(similarity, testcase1,testcase2)

            token1 = doc1[1]
            token2 = doc2[1]
            similarity = token1.similarity(token2)
            print(similarity, token1.text, token2.text)
