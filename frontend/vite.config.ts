import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Get repo name from environment or use default GitHub Pages repository name
const repoName = process.env.VITE_REPO_NAME || 'SAKHA-2'
const basePath = process.env.NODE_ENV === 'production' ? `/${repoName}/` : '/'

export default defineConfig({
  base: basePath,
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser'
  }
})
