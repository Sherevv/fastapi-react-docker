import * as path from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { ViteWebfontDownload } from 'vite-plugin-webfont-dl';


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    ViteWebfontDownload([
      'https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&display=swap',
    ]),
  ],
  server: {
    host: '0.0.0.0',
    port: 3001,
  },
  resolve: {
    alias: [
        { find: /^~/, replacement: '' },
        { find: '@', replacement: '/src'}
      ]
  },
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
      },
      scss: {},
    },
    modules: {
      localsConvention: 'camelCase',
    },
  },
})
