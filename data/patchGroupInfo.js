var fs = require('fs');

function patch(inputFile, outputFile, groupsFile = '', findTopGroup = true) {
    var json = fs.readFileSync(inputFile, 'utf8');
    var root = JSON.parse(json);
    
    var groups = [];
    for (var command in root) {
        if (!root[command].parameters) {
            groups.push(command);
        }
    }
    groups.sort();
    if (!findTopGroup) {
        groups.reverse();
    }

    var outputGroups = [];
    
    for (var command in root) {
        var group = groups.find(g => g === command || command.startsWith(g + ' '));
        if (group) {
            root[command].group = group;
            if (!outputGroups.includes(group)) {
                outputGroups.push(group);
            }
        } else {
            root[command].group = command;
            if (!outputGroups.includes(command)) {
                outputGroups.push(command);
            }
        }
    }
    
    outputGroups.sort();

    fs.writeFileSync(outputFile, JSON.stringify(root, 0, 4));
    if (groupsFile) {
        fs.writeFileSync(groupsFile, outputGroups.join('\n'));
    }
}

patch('./help_dump_small.json', './help_dump_small_with_top_group.json', './top_groups_small.txt');
patch('./help_dump_small.json', './help_dump_small_with_sub_group.json', './sub_groups_small.txt', false);
patch('./help_dump.json', './help_dump_with_top_group.json', './top_groups.txt');
patch('./help_dump.json', './help_dump_with_sub_group.json', './sub_groups.txt', false);