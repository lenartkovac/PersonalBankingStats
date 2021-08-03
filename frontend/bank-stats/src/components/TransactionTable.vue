<template lang="html">
	<table class="fl-table">
		<!-- Table head -->
		<thead>
			<tr>
				<th>index</th>
				<th @click="switchSort('name')">
					<span>title</span>
					<span v-if="sorting === 'name'">
						<span :key="reversed"><i :class="reversed ? 'fas fa-sort-up' : 'fas fa-sort-down'"/></span>
					</span>
				</th>
				<th @click="switchSort('value')">
					<span>value</span>	
					<span v-if="sorting === 'value'">
						<span :key="reversed"><i :class="reversed ? 'fas fa-sort-up' : 'fas fa-sort-down'"/></span>
					</span>
				</th>
				<th v-if="categorized">
					<span>EDIT</span>
				</th>
			</tr>
		</thead>
		<!-- Table body -->
		<tbody>
			<tr v-for="(name, index) in getKeys()" :key="index">
				<td>{{index + 1}}</td>
				<td>{{name}}</td>
				<td>{{round(data[name])}}€</td>

				<td v-if="changing === name" class="changeSelect">
					<CategorySelect
					@selection="changeCategory($event, title, name)"
					:currCategory="title"/>
				</td>
				<td
				v-else-if="categorized"
				@click="changeClick(name)">
					<i class="fas fa-edit"/>
				</td>
			</tr>
		</tbody>
		<!-- Table footer -->
		<tfoot>
			<tr>
				<!--<td>x</td>-->
				<td colspan="2">total {{title}}</td>
				<td>{{round(total)}}€</td>
			</tr>
		</tfoot>
	</table>
</template>

<script>
import CategorySelect from './CategorySelect.vue'

export default {
	name: "TransactionTable",
	components: {
		CategorySelect
	},
	emits: ['categoryChange'],
	props: {
		data: {
			type: Object,
			default: null
		},
		title: {
			type: String,
			default: ''
		},
		categorized: {
			type: Boolean,
			default: false
		}
	},
	data() {
		return {
			idx: 0,
			sorting: "name",
			reversed: true,
			changing: ""
		}
	},
	methods: {
		round(num) {
			return Math.round(num * 100) / 100;
		},
		index() {
			this.idx++;
			return this.idx - 1;
		},
		getKeys() {
			//let array = []
			if (this.data == null) {
				return []
			}
			const sortFunction = this.sorting === "name" ? undefined : (a, b) => {
				if (this.data[a] < this.data[b]) 
					return -1;
				if (this.data[a] > this.data[b])
					return 1;
				return 0;
			};

			const array = Object.keys(this.data).sort(sortFunction);

			return this.reversed ? array.reverse() : array;
		},
		changeSort() {
			this.sorting = this.sorting === "name" ? "value" : "name";
		},
		changeOrder() {
			this.reversed = !this.reversed;
			//console.log(this.reversed)
		},
		switchSort(origin) {
			if (origin === this.sorting)
				this.changeOrder()
			else 
				this.changeSort()
		},
		changeClick(name) {
			this.changing = name;
			//console.log(this.changing);
		},
		changeCategory(newCategory, currCategory, name) {
			//console.log(newCategory, currCategory, name)
			//console.log(typeof(newCategory))
			this.changing = "";
			this.$emit('categoryChange', {name, currCategory, newCategory})
		}
	},
	computed: {
		total: function() {
			if (!this.data || this.data == {}) {
				return 0;
			}

			let total = 0;
			for (let val in this.data) {
				total += this.data[val];
			}
			return total;
		}
	}
}
</script>

<style scoped>
/* Table Styles */
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

.changeSelect {
	width: 25%;
}

/* Responsive */

/*
@media (max-width: 767px) {
    .fl-table {
        display: block;
        width: 100%;
    }
    .table-wrapper:before{
        content: "Scroll horizontally >";
        display: block;
        text-align: right;
        font-size: 11px;
        color: white;
        padding: 0 0 10px;
    }

    .fl-table thead, .fl-table tbody, .fl-table thead th {
        display: block;
    }

    .fl-table thead th:last-child{
        border-bottom: none;
    }

    .fl-table thead {
        float: left;
    }

    .fl-table tbody {
        width: auto;
        position: relative;
        overflow-x: auto;
    }

    .fl-table td, .fl-table th {
        padding: 20px .625em .625em .625em;
        height: 60px;
        vertical-align: middle;
        box-sizing: border-box;
        overflow-x: hidden;
        overflow-y: auto;
        width: 120px;
        font-size: 13px;
        text-overflow: ellipsis;
    }

    .fl-table thead th {
        text-align: left;
        border-bottom: 1px solid #f7f7f9;
    }

    .fl-table tbody tr {
        display: table-cell;
    }

    .fl-table tbody tr:nth-child(odd) {
        background: none;
    }

    .fl-table tr:nth-child(even) {
        background: transparent;
    }

    .fl-table tr td:nth-child(odd) {
        background: #F8F8F8;
        border-right: 1px solid #E6E4E4;
    }

    .fl-table tr td:nth-child(even) {
        border-right: 1px solid #E6E4E4;
    }

    .fl-table tbody td {
        display: block;
        text-align: center;
    }
}
*/

.fl-table tfoot {
	border-top: 0.1em solid black;
}
</style>