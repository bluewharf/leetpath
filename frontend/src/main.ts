import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from './router'
import '@fontsource-variable/inter'
import '@fontsource-variable/jetbrains-mono'
import 'katex/dist/katex.min.css'
import './styles/index.css'
import { initTheme } from './theme'
import { initFontSize } from './stores/pref'

initTheme()
initFontSize()

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
