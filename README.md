# Install "Hey"
Run following in Cloud Shell:

[![Launch Cloud Shell](https://shell.azure.com/images/launchcloudshell.png "Launch Cloud Shell")](https://shell.azure.com)

```
mkdir -p bin && curl -sL https://github.com/ningliaoyuan/smartcloudshell/releases/download/v0.11/smartcloudshell_linux_64-bit.tar.gz | tar xz && mv ./hey ./bin && export PATH=$PATH:~/bin
```

Try Hey like:
```
hey list all my vms in east us
```

```
hey deploy a docker container
```

```
hey tell me a joke
```

# Developers Instructions

## Setup

- pip install -r requirements.txt
- python -m spacy download en_core_web_lg
- python -m spacy download en_core_web_sm

## How to run server

```bash
python main.py
```

Then user the follow url to test:
<http://localhost:80/cli/help/your%20query>

```bash
python test.py
```

Then check out the output in output folder

## Build server Docker image

```bash
docker build -t smartcloudshell .
```

## Run server Docker image

```bash
docker run -p 80:80 smartcloudshell
```

# Build Hey
```
export GOPATH=$PWD/client && cd ./client/src/hey
go build
```

Run hey with debug
```
hey -d create vm
```

# Azure Api

```
curl http://heyapi.trafficmanager.net/q/tell%20me%20a%20joke?custom=true
```