import numpy as np

def getVector(vocab, words):
  tokens = words.split(' ')
  vectors = list(map(vocab.get_vector, tokens))
  return np.mean(vectors, axis = 0)

def updateDocVector(doc):
  # The original implementation: https://github.com/explosion/spaCy/blob/e0caf3ae8c5a1d7fe79bae7e7d04ec2b31fc7561/spacy/tokens/doc.pyx
  tokenVectors = []
  for token in doc:
    if(token.is_oov):
      vector = getVector(doc.vocab, token.text)
      # TODO: Add 3 times to increase weight
      tokenVectors.append(vector)
      tokenVectors.append(vector)
      tokenVectors.append(vector)
    else:
      tokenVectors.append(token.vector)

  doc.vector = np.mean(tokenVectors, axis = 0)
