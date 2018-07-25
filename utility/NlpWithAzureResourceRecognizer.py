from utility.AzureResourceRecognizer import AzureResourceRecognizer
import en_core_web_lg as model_lg

print("Create nlpWithAzureResourceRecognizer")
nlp = model_lg.load()
azureResourceRecognizer = AzureResourceRecognizer(nlp)
nlp.add_pipe(azureResourceRecognizer, last=True)

def nlpWithAzureResourceRecognizer():
    return nlp