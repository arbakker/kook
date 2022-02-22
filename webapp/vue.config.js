const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: './',
  productionSourceMap: process.env.NODE_ENV != 'production',
  transpileDependencies: [
    'vuetify'
  ]
})
