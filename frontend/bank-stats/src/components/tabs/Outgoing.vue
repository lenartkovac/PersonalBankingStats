<template>
	<div v-if="dataError">
		<Error :message="dataError" @reload="handleReload" />
	</div>
	<div v-else>
		<TransactionTable v-bind:data="data" title="outgoing"/>
	</div>
</template>

<script>
import TransactionTable from '@/components/reusables/TransactionTable.vue';
import Error from '@/components/reusables/Error.vue';
import { API_URL } from '@/assets/constants';

export default {
	name: 'Outgoing',
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
			title: 'Outgoing',
			dataError: '',
			data: {}
		};
	},
	methods: {
		loadData() {
			this.axios.get(`${API_URL}/transactions/${this.date.getFullYear()}/${this.date.getMonth() + 1}/outgoing`)
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
			this.loadData();
		}
	},
	mounted() {
		this.loadData();
	}
};
</script>

<style scoped>
</style>