<template>
	<div v-if="error">
		{{error}}
	</div>
	<div v-else>
		<TransactionTable v-bind:data="data"/>
	</div>
</template>

<script>
import TransactionTable from '../TransactionTable.vue'
export default {
	name: "Incoming",
	components: {
		TransactionTable
	},
	props: {
		month: {
			type: Number,
			default: 0
		}
	},
	data() {
		return {
			title: "Incoming",
			data: {},
			error: null
		}
	},
	mounted() {
		this.axios.get(`http://localhost:5000/api/v1/transactions/${this.month}/incoming`)
			.then((response) => {
				if (!response 
				|| !response.data 
				|| response.data.status !== "OK" 
				|| !response.data.data) {
					this.error = "Error retrieving data"
				}
				this.data = response.data.data
			})
	}
}
</script>

<style>
</style>