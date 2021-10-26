<template>
	<div class="container mar-top">
		<h1>Categories</h1>
		<div v-if="dataError">
			<Error :message="dataError" @reload="handleReload" />
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

			<div class="delError" v-if="deleteError">
				<span>{{deleteError}}</span>
			</div>
			<br>

			<!-- new category input -->
			<div class="addCategory">
				<input class="inputField" type="input" name="addCategory" id="addCategory" @input="clearInputError" v-model="message" placeholder="test" required/>
				<label class="inputLabel noSelect" for="addCategory">Enter new category</label>
				<button @click="addCategory(message)">Add category</button>
			</div>
			
			<div class="inputError" v-if="inputError">
				<span>{{inputError}}</span>
			</div>
		</div>
	</div>
</template>

<script>
import Error from '@/components/reusables/Error.vue';
import '@/assets/style.css';
import { API_URL } from '@/assets/constants';

export default {
	name: 'Settings',
	components: {
		Error
	},
	data() {
		return {
			data: null,
			message: '',
			dataError: null,
			deleteError: '',
			inputError: '',
		};
	},
	methods: {
		handleReload() {
			this.dataError = '';
			this.loadCategoryNames();
		},
		addCategory(catName) {

			if (catName.length < 1) {
				this.inputError = 'Category name cannot be empty';
				return;
			}

			if(this.data.find(el => el === catName)) {
				this.inputError = 'This category already exists';
				return;
			}

			let payload = {};
			payload[catName] = '';

			const loader = this.$loading.show({
				container: null,
				color: '#4FC3A1',
				loader: 'dots',
				backgroundColor: '#000'
			});

			this.axios.post(`${API_URL}/categories`, payload)
				.then(response => {
					if (!response
					|| !response.data
					|| response.data.status !== 'OK'
					|| !response.data.data) {
						this.dataError = 'Error retreiving data';
					}
				})
				.catch(error => {
					this.inputError = error.message;
				})
				.finally(() => {
					setTimeout(() => {
						loader.hide();
						this.loadCategoryNames();
					}, 250);
				});
			this.message = '';
		},
		removeCategory(catName) {
			const loader = this.$loading.show({
				container: null,
				color: '#4FC3A1',
				loader: 'dots',
				backgroundColor: '#000'
			});

			this.axios.delete(`${API_URL}/categories/${catName}/delete`)
				.then(response => {
					if (!response || response.status !== 204) {
						if (response.data && response.data.error) {
							this.deleteError = response.data.error;
						} else {
							this.deleteError = 'Error deleting category';
						}
						return;
					}
				})
				.catch(error => {
					if (error.response && error.response.data && error.response.data.error) {
						this.deleteError = error.response.data.error;
						return;
					}
					this.deleteError = error.message;
				})
				.finally(() => {
					setTimeout(() => {
						loader.hide();
						this.loadCategoryNames();
					}, 250);
				});
		},
		loadCategoryNames() {
			const loader = this.$loading.show({
				container: null,
				color: '#4FC3A1',
				loader: 'dots',
				backgroundColor: '#000'
			});

			this.axios.get(`${API_URL}/categories/names`)
				.then(response => {
					if (!response 
					|| !response.data 
					|| response.data.status !== 'OK' 
					|| !response.data.data) {
						this.dataError = 'Error retrieving data';
					}
					this.data = response.data.data.filter(el => el !== 'other').sort();
				})
				.catch(error => {
					if (error.response && error.response.data && error.response.data.error) {
						this.dataError = error.response.data.error;
						return;
					}
					this.dataError = error.message;
				})
				.finally(() => {
					setTimeout(() => loader.hide(), 250);
				});
		},
		clearInputError() {
			this.inputError = '';
		}
	},
	mounted() {
		this.loadCategoryNames();
	}
};

</script>


<style scoped>

h1 {
	margin-left: 5%;
}

.mar-top {
	margin-top: 4em;
}

.addCategory {
	display: flex;
	width: 75%;
	margin-bottom: 0.2em;
	margin-left: 25%;
	position: relative;
}

.inputField {
	border: 0;
	border-bottom: 2px solid lightgray;
	outline: 0;
	transition: border-color 0.2s;
	margin-right: 0.5em;
}

.inputField::placeholder {
	color: transparent;
}

.inputField:placeholder-shown ~ .inputLabel {
	bottom: 1px;
	left: 5px;
	font-size: 14px;
}

.inputLabel {
	position: absolute;
	bottom: 20px;
	font-size: 12px;
	transition: all 0.2s ease-in-out;
}

.inputField:focus {
	border-color: #4FC3A1;
}

.inputField:focus ~ .inputLabel {
	color: #4FC3A1;
	bottom: 20px;
	left: 0;
	font-size: 12px;
}

button {
	background-color: white;
	border-radius: 0.3em;
	border: 1px solid lightgray;
	box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
}

button:hover {
	background-color: #4FC3A1;
	color: white;
	border-color: #4FC3A1;
}

.inputError, .delError {
	background: rgba(255, 0, 0, 0.6);
	margin: 0.1em auto ;
	padding: 0.2em 2em;
	border-radius: 0.5em;

	text-align: center;
	width: fit-content;
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