import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/tailwind.css';
import Toast, { POSITION } from 'vue-toastification';
import 'vue-toastification/dist/index.css'; 
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";


const app = createApp(App);
app.use(ElementPlus);
app.use(Toast, {
    position: POSITION.TOP_LEFT,
    timeout: 5000,
    zIndex: 2147483647
  });

// Enable devtools in production
app.config.devtools = true;

console.log('API URL:', process.env.VUE_APP_API_URL);


app.use(router).mount('#app');