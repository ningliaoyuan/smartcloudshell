# Setup
- pip install -r requirements.txt
- python -m spacy download en_core_web_lg
- python -m spacy download en_core_web_sm


# install packages on azure web app
D:\home\python364x64\Scripts\pip install -r requirements.txt

# Build whl files. Only use this when introduce new packages.
# We need to generate whl files because Azure Web App doens't have c++ compiler available.
pip wheel -r requirements.txt -w wheelhouse
