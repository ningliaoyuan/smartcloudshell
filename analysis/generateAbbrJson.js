var fs = require('fs');


function getWordCountsDic() {
    var helpText = fs.readFileSync("../data/help_dump.json", 'utf8');
    helpText = helpText
        .replace(/[^\w\s]/gi, '')
        .replace(/ +(?= )/g, '')
        .toLowerCase();

    var lines = helpText.split("\n");

    var tokens = helpText.split(" ");
    var dic = {};
    for (var i = 1, len = tokens.length; i < len; i++) {
        var word = tokens[i];
        if (dic[word]) {
            dic[word] = 0;
        }

        dic[word]++;
    }

    return dic;
}

function run() {
    // var wordCounts = getWordCountsDic(); // TODO
    var text = fs.readFileSync('abbr.csv', 'utf8');
    var lines = text.split("\n");

    var result = {};
    for (var i = 1, len = lines.length; i < len; i++) {
        var line = lines[i];
        var tokens = line.split(',');
        var abbr = tokens[0];
        var word = tokens[1];
        var count = parseInt(tokens[7]);
        if (word && abbr) {
            result[abbr.toLowerCase()] = { word: word.toLowerCase(), count: count };
        }
    }

    fs.writeFileSync("../data/abbr.json", JSON.stringify(result, 0, 4));
}

run();