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

# export path to include hey
```
vim .bashrc
export PATH=$PATH:~/bin
source .bashrc
```