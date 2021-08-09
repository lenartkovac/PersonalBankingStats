<template>
	<div class="container">
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
			<table class="fl-table">
				<thead>
					<tr>
						<th>category name</th>
						<th>delete</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(name, idx) in data" :key="idx">
						<td>{{name}}</td>
						<td @click="removeCategory(name)"><i class="fas fa-times"/></td>
					</tr>
				</tbody>
			</table>

			<br>

			<!-- new category input -->
			<div class="addCategory">
				<input @input="clearInputError" v-model="message" placeholder="enter new category"/>
				<button  @click="addCategory(message)">Add category</button>
			</div>

			<div class="error" v-if="inputError">
				<span>{{inputError}}</span>
			</div>
		</div>
	</div>
</template>

<script>
import '@/assets/style.css'

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

h1 {
	margin-left: 5%;
}

.error {
	background: rgba(255, 0, 0, 0.6);
	padding: 0.2em;
	margin-top: 0.3em;
	border-radius: 0.3em;

	text-align: center;
	width: fit-content;
}

.errmsg {
	margin-bottom: 1em;
}

input {
	margin-bottom: 0.3em;
}

.addCategory {
	display: flex;
	/*
	align-content: center;
	*/
	justify-content: center;
}

table {
	border-spacing: 10px;
	border-collapse: separate;
}

.table-wrapper{
    margin: 10px 70px 70px;
    box-shadow: 0px 35px 50px rgba( 0, 0, 0, 0.2 );
}

.fl-table {
    border-radius: 5px;
    font-size: 12px;
    font-weight: normal;
    border: none;
    border-collapse: collapse;
    width: 100%;
    max-width: 100%;
    white-space: nowrap;
    background-color: white;
}

.fl-table td, .fl-table th {
    text-align: center;
    padding: 8px;
}

.fl-table td {
    border-right: 1px solid #f8f8f8;
    font-size: 12px;
}

.fl-table thead th {
    color: #ffffff;
    background: #4FC3A1;
}

.fl-table thead th:nth-child(odd) {
    color: #ffffff;
    background: #324960;
}

.fl-table tr:nth-child(even) {
    background: #F8F8F8;
}

</style>