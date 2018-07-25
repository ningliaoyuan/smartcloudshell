# download and unzip binary
## init download folder and bin folder
``` bash
mkdir Downloads
mkdir bin
```
## download and extract
```
curl -L https://github.com/ningliaoyuan/smartcloudshell/releases/download/v0.5/smartcloudshell_linux_64-bit.tar.gz -o ./Downloads/smartCloudShell.tar.gz
tar -xvzf ./Downloads/smartCloudShell.tar.gz -C ./bin
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