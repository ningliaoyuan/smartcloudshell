# Setup
- pip install -r requirements.txt
- python -m spacy download en_core_web_lg
- python -m spacy download en_core_web_sm



# How to use:

- python main.py

Then user the follow url to test:
http://localhost:5000/cli/help/your query

- python test.py
Then check out the output in output folder

# Install packages on azure web app

Build whl files. Only use this when introduce new packages.
We need to generate whl files because Azure Web App doens't have c++ compiler available.

Remote:
- D:\home\python364x64\Scripts\pip install -r requirements.txt

Local:
- pip wheel -r requirements.txt -w wheelhouse
