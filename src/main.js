import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

//createApp(App).use(router).mount('#app').use(store);
const app = createApp(App);
app.use(store);
app.use(router);
app.mount('#app');
