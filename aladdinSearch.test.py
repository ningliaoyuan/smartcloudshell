from aladdinSearch import AladdinSearch

aladdin = AladdinSearch()
promise = aladdin.search("managementGroup")
results = aladdin.resolveRequest(promise)

doc1 = results[0]
print(doc1['title'])
print(doc1['link'])
print(doc1['snippet'])