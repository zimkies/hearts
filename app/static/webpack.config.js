const webpack = require('webpack');
const config = {
    entry:  __dirname + '/scripts/index.js',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    mode: 'development',
    devtool: 'inline-source-map',
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },

    module: {
        rules: [
            {
            test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: 'babel-loader'
            },
            {
                // look for .css or .scss files
                test: /\.(css|scss)$/,
                exclude: /node_modules/,
                use: [
                  {
                    loader: 'style-loader',
                  },
                  {
                    loader: 'css-loader',
                  },
                  {
                    loader: 'sass-loader',
                    options: {
                      sourceMap: true,
                    },
                  },
                ],
            },
            {
              test: /\.svg$/,
              use: ['@svgr/webpack'],
            },
        ]
    }
};
module.exports = config;
