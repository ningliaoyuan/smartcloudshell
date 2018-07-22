import spacy, time
from log import log
from data import cliData, cliData_partial, cliData_sm
from modelBase import CliNlpModel

import en_core_web_lg as model_lg
import en_core_web_sm as model_sm

class Model:
  def __init__(self, data, model, id, desc = None):
    self._data = data
    self._model = model
    self.id = id
    self._desc = desc

  def load(self) -> CliNlpModel:
    op0 = log().start("loading model: " + self._desc)

    op = log().start("loading model")
    nlp = self._model.load()
    op.end("loaded")

    op = log().start("loading baseline model")
    cliModel = CliNlpModel(self.id, self._data, nlpModel = nlp, rewriteQuery = lambda q:q)
    op.end("loaded")

    op0.end("finish loading model")
    return cliModel

baselineModel_sm = Model(cliData_sm, model_sm, "smd_smm_nqr", "small data set with small nlp model")
baselineModel_lg = Model(cliData, model_lg, "lgd_lgm_nqr", "large data set with large nlp model")
baselineModel_partial = Model(cliData_partial, model_lg, "pad_lgm_nqr", "partial data set with large nlp model")

# sm = baselineModel_sm.load()
# suggestions = sm.getSuggestions("create storage account")
# print(suggestions)
