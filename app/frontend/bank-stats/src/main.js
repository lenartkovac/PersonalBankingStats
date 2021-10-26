import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import store from './store';
import router from './router';
import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';
import VueLoading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

const app = createApp(App);
app.use(VueAxios, axios);
app.use(store);
app.use(router);
app.use(VueLoading);
app.directive('invisible', {
	mounted: (el, binding) => {
		el.style.visibility = binding.value ? 'hidden' : 'visible';
	},
	updated: (el, binding) => {
		el.style.visibility = binding.value ? 'hidden' : 'visible';
	}
});
app.mount('#app');