var fs = require('fs');

var json = fs.readFileSync('data/help_dump.json', 'utf8');
var root = JSON.parse(json);

function addToDic(key, dic, command) {
    if (!dic[key]) {
        dic[key] = [];
    }

    dic[key].push(command);
}

var lastWordDic = {};
var firstWordDic = {};
for (var command in root) {
    var tokens = command.split(' ');
    var lastWord = tokens[tokens.length - 1].toLowerCase();
    addToDic(lastWord, lastWordDic, command);

    var firstWord = tokens[0];
    addToDic(firstWord, firstWordDic, command);
}

fs.writeFileSync("data/lastWord.json", JSON.stringify(lastWordDic, 0, 4));
fs.writeFileSync("data/firstWord.json", JSON.stringify(firstWordDic, 0, 4));
console.log("completed")
