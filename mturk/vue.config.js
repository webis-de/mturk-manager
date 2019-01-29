const webpack = require('webpack');

module.exports = {
    runtimeCompiler: true,
    outputDir: 'mturk_manager/static/mturk_manager/js/dist',
    indexPath: '../../../../../mturk_manager/templates/mturk_manager/app.html',
    configureWebpack: {
        plugins: [
            new webpack.ContextReplacementPlugin(/moment[/\\]locale$/, /en-gb/),
        ]
    }
}