# download and unzip binary

## download and extract
```
mkdir bin && curl -sL https://github.com/ningliaoyuan/smartcloudshell/releases/download/v0.8/smartcloudshell_linux_64-bit.tar.gz | tar xz && mv ./hey ./bin && export PATH=$PATH:~/bin
```

# append following script to ~/.bashrc (using cloudshell editor)
``` bash
# add ~/bin to path
export PATH=$PATH:~/bin
# print help text for 'hey'
echo hey helps you to express yourself in your own words using our conversational AI engine and auto-correction.
echo
echo For example: Search by typing: "hey update the file in storage" or "hey create new storage directory"
echo To learn more about the supported skills: hey -help
```

# reload ~/.bashrc
```bash
source ~/.bashrc
```