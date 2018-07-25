from AzureResourceRecognizer import AzureResourceRecognizer
import en_core_web_lg as model_lg

class NlpWithAzureResourceRecognizer:
  def __init__(self):
    self._nlp = None

  def load(self):
    if self._nlp is None:
      print("Create nlpWithAzureResourceRecognizer")
      nlp = model_lg.load()
      azureResourceRecognizer = AzureResourceRecognizer(nlp)
      nlp.add_pipe(azureResourceRecognizer, last=True)
      self._nlp = nlp

    return self._nlp