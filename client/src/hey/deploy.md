# download and unzip binary

## download and extract
```
mkdir -p bin && curl -sL https://github.com/ningliaoyuan/smartcloudshell/releases/download/v0.11/smartcloudshell_linux_64-bit.tar.gz | tar xz && mv ./hey ./bin && export PATH=$PATH:~/bin
```

# append following script to ~/.bashrc

try cloudshell editor:
code ~/.bashrc

``` bash
# add ~/bin to path
export PATH=$PATH:~/bin
# print help text for 'hey'
echo Try "hey" to learn how to interactive with Azure in Natural Language
echo
echo Examples:
echo   hey show my subscriptions
echo   hey create a storage account
echo   hey list my linux vms
echo   hey tell me a joke
```

# reload ~/.bashrc
```bash
source ~/.bashrc
```