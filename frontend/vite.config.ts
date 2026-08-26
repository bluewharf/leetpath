import { readFileSync } from 'node:fs'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 版本号单源为仓库根目录 VERSION；Docker 构建时由 LEETPATH_VERSION 环境变量注入
function readAppVersion(): string {
  if (process.env.LEETPATH_VERSION) return process.env.LEETPATH_VERSION
  try {
    return readFileSync(new URL('../VERSION', import.meta.url), 'utf-8').trim()
  } catch {
    return 'dev'
  }
}

export default defineConfig({
  plugins: [vue()],
  define: {
    __APP_VERSION__: JSON.stringify(readAppVersion()),
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          const p = id.replace(/\\/g, '/')
          if (!p.includes('node_modules')) return
          // 编辑器只随做题页按需加载
          if (/node_modules\/(@codemirror|@lezer|codemirror)\//.test(p)) return 'codemirror'
          // markdown/katex 渲染栈单独成块
          if (/node_modules\/(marked|marked-katex-extension|katex|dompurify)\//.test(p)) return 'markdown'
          if (/node_modules\/(vue|vue-router|pinia|@vue)\//.test(p)) return 'vendor'
        },
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
