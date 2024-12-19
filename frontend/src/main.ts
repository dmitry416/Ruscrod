import './assets/main.css'
import CarbonVue3 from '@carbon/vue'
import 'carbon-components/css/carbon-components.min.css';
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)
app.use(CarbonVue3)

app.mount('#app')