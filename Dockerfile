FROM python:3.6

WORKDIR /usr/src/app

RUN pip install spacy==2.0.0
RUN python -m spacy download en_core_web_lg
RUN python -m spacy download en_core_web_sm

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]
