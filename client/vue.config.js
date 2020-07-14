const path = require('path');

module.exports = {
    devServer: {
        proxy: {
            '^/': {
                target: 'http://127.0.0.1:5000'
            }
        }
    },
    outputDir: path.resolve(__dirname, '../bookmarks/templates'),
    assetsDir: 'static',
};
