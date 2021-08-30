<template lang="html">
	<table class="fl-table">
		<!-- Table head -->
		<thead class="noSelect">
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
				<td :class='{categorized: "categorized"}' >{{index + 1}}</td>
				<td :class='{categorized: "categorized"}'>{{name}}</td>
				<td :class='{categorized: "categorized"}'>{{round(data[name])}}€</td>

				<td v-if="changing === name" class="categorized">
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
import CategorySelect from '@/components/reusables/CategorySelect.vue'
import '@/assets/style.css'

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
		},
		switchSort(origin) {
			if (origin === this.sorting)
				this.changeOrder()
			else 
				this.changeSort()
		},
		changeClick(name) {
			this.changing = name;
		},
		changeCategory(newCategory, currCategory, name) {
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

.fl-table {
    border-radius: 1.2em;
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

.fl-table .categorized {
	width: 25%
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

.fl-table tfoot {
	border-top: 0.1em solid black;
}
</style>