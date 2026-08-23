import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from './router'
import '@fontsource-variable/inter'
import '@fontsource-variable/jetbrains-mono'
import '@fontsource-variable/noto-serif-sc'
import './styles.css'
import { initTheme } from './theme'

initTheme()

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
