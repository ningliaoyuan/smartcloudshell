REM Build whl files. Only use this when introduce new packages.
REM We need to generate whl files because Azure Web App doens't have c++ compiler available.
pip wheel -r requirements.txt -w wheelhouse
