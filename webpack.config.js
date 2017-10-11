const path = require('path');

module.exports = {
  entry: './_scripts/index.js',
  output: {
    filename: 'script.js',
    path: path.resolve(__dirname, 'assets')
  },
  externals: {
    jquery: 'jQuery'
  }
};

