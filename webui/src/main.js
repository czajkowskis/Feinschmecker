import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import axios from '../services/axios.js';
import { MotionPlugin } from '@vueuse/motion'
import router from './router'
const app = createApp(App)

app.config.globalProperties.$axios = axios;
app.use(MotionPlugin);
app.use(router)
app.mount('#app')
