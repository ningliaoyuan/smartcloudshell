
# Setup

- pip install -r requirements.txt
- python -m spacy download en_core_web_lg
- python -m spacy download en_core_web_sm

# How to use

```bash
python main.py
```

Then user the follow url to test:
<http://localhost:80/cli/help/your%20query>

```bash
python test.py
```

Then check out the output in output folder

# Build Docker image

```bash
docker build -t smartcloudshell .
```

# Run Docker image

```bash
docker run -p 5000:5000 smartcloudshell
```

# Install Hey

Windows
```
https://github.com/ningliaoyuan/smartcloudshell/releases/download/v0.3/smartcloudshell_windows_64-bit.zip
```

Run with debug
```
hey -d create vm
```

# Azure Api

<http://heyapi.trafficmanager.net>

<http://heyapi.trafficmanager.net/cli/help/create%20vm>

<http://smartcloudshellapi.westus2.azurecontainer.io/cli/help/I%20want%20to%20create%20a%20storage%20account>