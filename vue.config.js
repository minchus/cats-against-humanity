module.exports = {
  'outputDir': 'dist',
  'assetsDir': 'static',
  'devServer': {
    'proxy': {
      '/info': {
        'target': 'http://localhost:5000/'
      },
      '/socket.io': {
        target: 'http://localhost:5000',
        ws: true,
        changeOrigin: true
      }
    }
  },
  'transpileDependencies': [
    'vuetify'
  ]
}
