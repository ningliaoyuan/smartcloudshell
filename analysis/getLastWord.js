var fs = require('fs');

var json = fs.readFileSync('../data/help_dump.json', 'utf8');
var root = JSON.parse(json);

var result = {};
for (var command in root) {
    var tokens = command.split(' ');
    var lastWord = tokens[tokens.length - 1].toLowerCase();
    if (!result[lastWord]) {
        result[lastWord] = [];
    }

    result[lastWord].push(command);
}

fs.writeFileSync("lastWord.json", JSON.stringify(result, 0, 4));
