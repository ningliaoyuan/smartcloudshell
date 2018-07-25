import json
from requests_futures.sessions import FuturesSession

class AladdinSearch(object):
  def __init__(self, aladdinEndpoint='https://aladdinservice-staging.azurewebsites.net/api/aladdin/generateCards'):
    self.aladdinEndpoint = aladdinEndpoint
    self.session = FuturesSession()

  def search(self, text):
    payload = { "paragraphText":"", "currentPageUrl":"", "context":"", "query":text }
    future_two = self.session.post(self.aladdinEndpoint, data=None, json=payload)
    return future_two

  def resolveRequest(self, searchPromise, timeout = 3, top = 3):
    response = searchPromise.result(timeout)
    if response.status_code == 200:
      results = json.loads(response.content)
      return results[:top]
    else:
      print("Unexpected response when calling search:", response)
    return []
