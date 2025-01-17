import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import axios from '../services/axios.js';

const app = createApp(App)

app.config.globalProperties.$axios = axios;
app.mount('#app')
