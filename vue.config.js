const path = require('path')

// https://cli.vuejs.org/config/
if(process.env.NODE_ENV === 'production') {
  module.exports = {
    publicPath: '/',
    outputDir: 'flask_app/templates',
    assetsDir: '../static',
  }
}
