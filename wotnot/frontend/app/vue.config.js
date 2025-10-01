const webpack = require('webpack');

module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(true),
        // define other feature flags here if needed
      }),
    ],
  },
  devServer: {
    allowedHosts: 'all',  // Disable host checking
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_URL || 'http://localhost:8000', // Load from .env
        changeOrigin: true,
        secure: false,
      },
    },
    // Ensure WebSocket uses 'wss://'
    client: {
      webSocketURL: 'wss://5543-2405-201-3004-d09d-e838-3470-27b1-6b78.ngrok-free.app.ngrok.io/ws', // Keep unchanged
    },
  },
};
