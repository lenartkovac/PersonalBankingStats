<template>
<div>
	<div v-if="!error">
		<div v-for="category in Object.keys(data)" :key="category">
			<h3>{{capitalize(category)}}</h3>
			<TransactionTable v-bind:data="data[category]" v-bind:title="category"/>
		</div>
	</div>
	<div v-if="error">
		<h3> {{error}}</h3>
	</div>
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
			title: "Categorized",
			data: {},
			error: null
		}
	},
	methods: {
		capitalize(title) {
			return title.charAt(0).toUpperCase() + title.slice(1);
		}
	},
	mounted() {
		console.log("CATEGORIZED CREATED")
		this.axios.get(`http://localhost:5000/api/v1/transactions/${this.month}/outgoing/categorized`)
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

<style scoped>

h3 {
	text-align: center;
}

</style>