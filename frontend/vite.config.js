import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: 3100,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      'ceal.domain.com',
      '.domain.com', // Allows all subdomains
    ],
    proxy: {
      '/api': {
        target: 'http://localhost:8100',
        changeOrigin: true,
      },
    },
  },
})
