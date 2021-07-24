<template>
	<div>
		<h1>Categories</h1>
		<div class="error" v-if="dataError">
			<div class="errmsg">
				<span>{{dataError}}</span>
			</div>
			<div class="reloadIcon">
				<i class="fas fa-sync"/>
			</div>

			<div class="reloadText">
				<span>reload page</span>
			</div>
		</div>
		<div v-else>
			<table>
				<tbody>
					<tr v-for="(name, idx) in data" :key="idx">
						<td>{{name}}</td>
						<td @click="removeCategory(name)"><i class="fas fa-times"/></td>
					</tr>
				</tbody>
			</table>

			<br>

			<input @input="clearInputError" v-model="message" placeholder="enter new category"/>
			<button  @click="addCategory(message)">Add category</button>

			<div v-if="inputError">
				<span class="error">{{inputError}}</span>
			</div>
		</div>
	</div>
</template>

<script>

export default {
	name: "Settings",
	data() {
		return {
			data: null,
			message: "",
			dataError: null,
			inputError: "",
		}
	},
	methods: {
		addCategory(catName) {

			if (catName.length < 1) {
				this.inputError = "Category name cannot be empty"
				return
			}

			if(this.data.find(el => el === catName)) {
				this.inputError = "This category already exists"
				return
			}

			let payload = {}
			payload[catName] = ""
			this.axios.post('http://localhost:5000/api/v1/categories', payload)
				.then(response => {
					if (!response
					|| !response.data
					|| response.data.status !== "OK"
					|| !response.data.data) {
						this.dataError = "Error retreiving data"
					}
					this.loadCategoryNames()
				})
				.catch(error => {
					this.inputError = error.message
				})
			this.message = ""
		},
		removeCategory(catName) {
			this.axios.delete(`http://localhost:5000/api/v1/categories/${catName}/delete`)
				.then(response => {
					//TODO: edge case error matching
					console.log(response)
					this.loadCategoryNames()
				})
				.catch(error => {
					this.inputError = error.message
				})
		},
		loadCategoryNames() {
			this.axios.get(`http://localhost:5000/api/v1/categories/names`)
				.then((response) => {
					if (!response 
					|| !response.data 
					|| response.data.status !== "OK" 
					|| !response.data.data) {
						this.error = "Error retrieving data"
					}
					this.data = response.data.data.sort()
				})
				.catch(error => {
					this.dataError = error.message
				})
		},
		clearInputError() {
			this.inputError = ""
		}
	},
	mounted() {
		this.loadCategoryNames()
	}
}

</script>


<style scoped>

.error {
	background: rgba(255, 0, 0, 0.6);
	padding: 0.2em;
	border-radius: 0.3em;
	text-align: center;
}

.errmsg {
	margin-bottom: 1em;
}

input {
	margin-bottom: 0.3em;
}

table {
	border-spacing: 10px;
	border-collapse: separate;
}

</style>