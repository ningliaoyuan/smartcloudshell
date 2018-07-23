import json
import spacy
import numpy
from spacy import displacy
from pprint import pprint
from pathlib import Path
import re
from spacy.vocab import Vocab
from AzureResourceRecognizer import AzureResourceRecognizer

nlp = spacy.load('en_core_web_lg')
azureResourceRecognizer = AzureResourceRecognizer(nlp)
nlp.add_pipe(azureResourceRecognizer, last=True)

def run():
    sentences = [
        u"Update a public IP address", 
        u"Update a public IP resource with a DNS name label and static allocation",
        u"Show me how to create a route filter",
        u"Lists all the container registries under the current subscription",
        u"Can I restore a server from SQL backup",
        u"Show me how to create website",
        u"Steps to set a predefined SSL policy",
        u"I need to create a new virtual machine",
    ]

    for sentence in sentences:
        doc = nlp(sentence)
        print(sentence)
        for token in doc:
            print(token.text, token.dep_, token.head.text, token.head.pos_,
                [child for child in token.children])

        # for np in doc.noun_chunks:
        #     if np.root.dep_ == "dobj":
        #         print(np.text)

        svg = displacy.render(doc, style='dep')
        file_name = '-'.join([w.text for w in doc if not w.is_punct]) + '.svg'
        output_path = Path('linguistic/' + file_name)
        output_path.open('w', encoding='utf-8').write(svg)
        print("completed")

run()