<template>
<div>
	<div v-if="dataError">
		<Error :message="dataError" @reload="handlReload"/>
	</div>
	<div v-else>
		<div v-for="category in displayCategories" :key="category">
			<h3>{{capitalize(category)}}</h3>
			<TransactionTable 
			@categoryChange="categoryChange"
			:data="data[category]"
			:categorized="true"
			:title="category"/>
		</div>
	</div>
	<div class="mar-bot"/>
</div>
</template>

<script>
import TransactionTable from '@/components/reusables/TransactionTable.vue';
import Error from '@/components/reusables/Error.vue';
import { API_URL } from '@/assets/constants';

export default {
	name: 'Incoming',
	components: {
		TransactionTable,
		Error
	},
	props: {
		date: {
			type: Object
		}
	},
	data() {
		return {
			title: 'Categorized',
			data: {},
			dataError: '',
		};
	},
	computed: {
		displayCategories: function() {
			let keys =  Object.keys(this.data);

			//? remove and append other at the end of the array
			let idx = keys.indexOf('other');
			if (idx > -1) {
				keys.splice(idx, 1);
				keys.push('other');
			}

			//? remove categories that don't have any entries in them
			keys = keys.filter(category => Object.keys(this.data[category]).length !== 0);
			return keys;
		}
	},
	methods: {
		capitalize(title) {
			return title.charAt(0).toUpperCase() + title.slice(1);
		},
		categoryChange({currCategory, newCategory, name}) {

			if (!currCategory || !newCategory || !name) {
				console.error('Incomplete payload: Expected keys: currCategory, newCategory, name!');
				return;
			}

			if(!this.data[currCategory] || !this.data[newCategory]) {
				console.error(`current or new category doesn't exist curr: ${currCategory} new: ${newCategory}`);
				return;
			}

			if (!this.data[currCategory][name]) {
				console.error(`${name} is not in ${currCategory}!`);
			}

			let payload = {
				'currentCategory': currCategory,
				'newCategory': newCategory,
				'name': name
			};
			this.axios.put(`${API_URL}/categories`, payload)
				.then(response => {
					if (!response 
					|| !response.data) {
						console.error('Error in the response for change');
					}

					if (response.data.status === 'OK') {
						let value = this.data[currCategory][name];
						delete this.data[currCategory][name];

						this.data[newCategory][name] = value;
					}
				})
				.catch(error => {
					console.error(error);
				});
			
		},
		loadCategories() {
			this.axios.get(`${API_URL}/transactions/${this.date.getFullYear()}/${this.date.getMonth() + 1}/outgoing/categorized`)
				.then(response => {
					if (!response 
					|| !response.data 
					|| response.data.status !== 'OK' 
					|| !response.data.data) {
						this.dataError = 'Error retrieving data';
					}
					this.data = response.data.data;
				})
				.catch(error => {
					if (error.response && error.response.data && error.response.data.error) {
						this.dataError = error.response.data.error;
						return;
					}
					this.dataError = error.message;
				});
		},
		handleReload() {
			this.dataError = '';
			this.loadCategories();
		}
	},
	mounted() {
		this.loadCategories();
	}
};
</script>

<style scoped>

h3 {
	text-align: center;
}

</style>