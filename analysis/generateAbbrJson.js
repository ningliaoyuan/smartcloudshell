var fs = require('fs');

function countWordsInStr(str, counts) {
    str = str
        .replace(/[?:=\-_.\/]/g, ' ')
        .replace(/[^\w\s]/gi, '')
        .replace(/[0-9]/g, '')
        .replace(/\n/g, " ")
        .replace(/ +(?= )/g, '')
        .toLowerCase();

    var tokens = str.split(" ");
    for (var i = 0, len = tokens.length; i < len; i++) {
        var word = tokens[i];
        if (word && word.length > 1) {
            // if(word == "defaultsecurityrulesaccess")
            //     debugger;
            if (!counts[word]) {
                counts[word] = 0;
            }

            counts[word]++;
        }
    }
}

function count(obj, counts) {
    if (!obj) {
        return;
    }

    if (typeof obj === "string") {
        countWordsInStr(obj, counts);
        return;
    }

    if (Array.isArray(obj)) {
        for (var i = 1, len = obj.length; i < len; i++) {
            count(obj[key], counts);
        }
    }

    for (var key in obj) {
        // if (key === "parameters") {
        //     continue;
        // }

        count(obj[key], counts);
    }
}

function getWordCountsDic() {
    var helpText = fs.readFileSync("../data/help_dump.json", 'utf8');
    // have to parse to obj to count the workd, since the helpText is too large and below code hang 
    //  var lines = helpText.split("\n");
    var root = JSON.parse(helpText);
    var counts = {};
    count(root, counts)
    var r = JSON.stringify(counts);
    fs.writeFileSync("../data/help_dump-word-frequencies.json", JSON.stringify(counts, null, 4));
    return counts;
}

function run() {
    var wordCounts = getWordCountsDic(); // TODO
    var text = fs.readFileSync('abbr.csv', 'utf8');
    var lines = text.split("\n");

    var result = {};
    for (var i = 1, len = lines.length; i < len; i++) {
        var line = lines[i];
        var tokens = line.split(',');
        var abbr = tokens[0];
        var word = tokens[1];
        if (word && abbr) {
            result[abbr.toLowerCase()] = { word: word.toLowerCase(), count: wordCounts[abbr] };
        }
    }

    fs.writeFileSync("../data/abbr.json", JSON.stringify(result, 0, 4));
    console.log("completed");
}

run();