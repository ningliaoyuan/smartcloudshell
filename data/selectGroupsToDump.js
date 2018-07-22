var fs = require('fs');

function select(inputFile, groupsFile, outputFile, numGroupsToInclude = 20) {
    var json = fs.readFileSync(inputFile, 'utf8');
    var root = JSON.parse(json);

    var txt = fs.readFileSync(groupsFile, 'utf8');
    var groups = txt.split('\n').slice(0, numGroupsToInclude);

    var result = {};

    for (var command in root) {
        if (groups.includes(root[command].group)) {
            result[command] = root[command];
        }
    }

    fs.writeFileSync(outputFile, JSON.stringify(result, 0, 4));
}

select('./help_dump_with_top_group.json', './top_groups.txt', './help_dump_with_top_group_partial.json');