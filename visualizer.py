import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import mpld3
from mpld3 import plugins
import matplotlib.cm as cm

from models import baselineModel_sm, baselineModel_lg

def visualize(modelLoader, title='Command confusion map'):
  records = []
  model = modelLoader.load()
  for nlpNode in model.nlpNodes:
      id = nlpNode.cliNode.id
      for query in nlpNode.nlpQueries:
          if query.has_vector:
              record = {
                  'vector': query.vector,
                  'command': id,
                  'query': query.text
              }
              records.append(record)

  embeddings = pd.DataFrame(records)

  tsne = TSNE(n_components=2, verbose=2, metric='cosine', method='exact', n_iter=5000,
              perplexity=20, random_state=1131)
  tsne_results = tsne.fit_transform(np.stack(embeddings.vector, axis=0))
  dfg = embeddings[['command', 'query']].copy()
  dfg['t-x'] = tsne_results[:,0]
  dfg['t-y'] = tsne_results[:,1]
  dfg['rank'] = (dfg['t-x']-dfg['t-x'].min())**2+(dfg['t-y']-dfg['t-y'].min())**2
  dfg['command-group'] = dfg['command'].str.split().str.get(0)
  commands = dfg.drop_duplicates(['command-group']).sort_values(['rank'])[['command-group']].reset_index(drop=True)
  commands['id'] = np.arange(0, len(commands), 1)
  dfg = dfg.merge(commands, on='command-group', how='inner')

  fig, ax = plt.subplots(figsize=(16,12))
  ax.set_facecolor('#7E7E7E')
  colors = cm.tab20.colors
  lastIdx = 0
  for cmd in commands['command-group']:
    data = dfg[dfg['command-group']==cmd]
    c = data['id'].apply(lambda x: colors[x%len(colors)])
    s = data['command-group'].apply(lambda x:50 if x==cmd else 10)
    pt = ax.scatter(data['t-x'], data['t-y'], c=c, label=cmd, s=s, alpha=0.7)
    labels = ["- %s | %s" %(a[0],a[1]) for a in zip(data['command-group'], data['query'])]
    tooltip = plugins.PointLabelTooltip(pt, labels=labels)
    mpld3.plugins.connect(fig, tooltip)

  ax.grid(color='white', linestyle='solid')
  chartBox = ax.get_position()
  ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.7, chartBox.height])
  lg=ax.legend(loc='upper left', bbox_to_anchor=(1,1.1), ncol=1, fancybox=0,
              prop={'family':'Arial', 'size':'14'})
  lg.set_title('Command groups', prop={'family':'Arial', 'size':'16'})
  for i, text in enumerate(lg.get_texts()):
    text.set_color(colors[i%len(colors)])
  ax.set_title(title, size=20)
  plt.savefig(title+'.pdf')
  # mpld3.save_html(fig, 'ConfusionMap.html')

  # import socket
  # import os
  # hostip=socket.gethostbyname(socket.gethostname())
  # if os.getenv("WIN-DOCKER") is None:
  #   hostip="0.0.0.0"
  # mpld3.show(ip=hostip)

visualize(baselineModel_sm, 'Command confusion map - small dataset with small model')
#visualize(baselineModel_lg, 'Command confusion map - large dataset with large model')