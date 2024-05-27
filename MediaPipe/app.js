const fs = require('fs');
const util = require('util');

// Rediriger la sortie de la console vers un fichier
const logFile = fs.createWriteStream('console.log', { flags: 'a' });
const logStdout = process.stdout;

console.log = function(...args) {
    logFile.write(util.format(...args) + '\n');
    logStdout.write(util.format(...args) + '\n');
};

// Exemple d'utilisation
console.log('Ce message sera écrit dans le fichier log.');
console.log({ key: 'value', anotherKey: 'anotherValue' });
