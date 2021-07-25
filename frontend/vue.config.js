const webpack = require('webpack'); // eslint-disable-line
const CircularDependencyPlugin = require('circular-dependency-plugin');
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin');

module.exports = {
  lintOnSave: false,
  // lintOnSave: process.env.NODE_ENV !== 'production' ? 'error' : false,
  runtimeCompiler: true,
  // publicPath: '/static/mturk_manager/js/dist',
  // outputDir: 'mturk_manager/static/mturk_manager/js/dist',
  // indexPath: '../../../../../mturk_manager/templates/mturk_manager/app.html',
  configureWebpack: {
    plugins: [
      new webpack.ContextReplacementPlugin(/moment[/\\]locale$/, /en-gb/),
      new CircularDependencyPlugin({
        // exclude detection of files based on a RegExp
        exclude: /a\.js|node_modules/,
        // add errors to webpack instead of warnings
        failOnError: true,
        // set the current working directory for displaying module paths
        cwd: process.cwd(),
      }),
      new VuetifyLoaderPlugin(),
      new webpack.DefinePlugin({
        'process.env': {
          VERSION_MTURK_MANAGER: JSON.stringify(process.env.VERSION_MTURK_MANAGER),
        },
      }),
    ],
    optimization: {
      splitChunks: {
        chunks: 'all',
      },
    },
    performance: {
      hints: false,
    },
  },
  pluginOptions: {
    webpackBundleAnalyzer: {
      openAnalyzer: false,
    },
  },
  css: {
    extract: process.env.NODE_ENV === 'production' ? {
      ignoreOrder: true,
    } : false,
  },
  // lintOnSave: 'error',
  // devServer: {
  //   overlay: {
  //     warnings: true,
  //     errors: true,
  //   },
  // },
};
