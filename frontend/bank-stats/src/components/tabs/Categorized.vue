<template>
<div>
	<div v-if="!error">
		<div v-for="category in displayCategories" :key="category">
			<h3>{{capitalize(category)}}</h3>
			<TransactionTable 
			@categoryChange="categoryChange"
			v-bind:data="data[category]"
			v-bind:categorized="true"
			v-bind:title="category"/>
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
	computed: {
		displayCategories: function() {
			let keys =  Object.keys(this.data)

			//? remove and append other at the end of the array
			let test = keys.indexOf("other")
			if (test > -1) {
				keys.push("other")
			}

			//? remove categories that don't have any entries in them
			keys = keys.filter(category => Object.keys(this.data[category]).length !== 0)
			return keys
		}
	},
	methods: {
		capitalize(title) {
			return title.charAt(0).toUpperCase() + title.slice(1);
		},
		categoryChange({currCategory, newCategory, name}) {

			if (!currCategory || !newCategory || !name) {
				console.error("Incomplete payload: Expected keys: currCategory, newCategory, name!")
				return
			}

			if(!this.data[currCategory] || !this.data[newCategory]) {
				console.error(`current or new category doesn't exist curr: ${currCategory} new: ${newCategory}`)
				return
			}

			if (!this.data[currCategory][name]) {
				console.error(`${name} is not in ${currCategory}!`)
			}

			let payload = {
				"currentCategory": currCategory,
				"newCategory": newCategory,
				"name": name
			}
			this.axios.put('http://localhost:5000/api/v1/categories', payload)
				.then(response => {
					if (!response 
					|| !response.data) {
						this.error = "Error making stuff"
						console.error("Error in the response for change")
					}

					if (response.data.status === "OK") {
						let value = this.data[currCategory][name]
						delete this.data[currCategory][name]

						this.data[newCategory][name] = value
					}
				})
				.catch(error => {
					console.error(error)
				})
			
		}
	},
	mounted() {
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