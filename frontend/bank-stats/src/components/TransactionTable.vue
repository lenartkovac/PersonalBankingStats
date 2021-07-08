<template lang="html">
	<table>
		<thead>
			<tr>
				<th>index</th>
				<th>title</th>
				<th>value</th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="(name, index) in getKeys()" :key="index">
				<td>{{index + 1}}</td>
				<td>{{name}}</td>
				<td>{{round(data[name])}}€</td>
			</tr>
		</tbody>
		<tfoot>
			<tr>
				<td></td>
				<td>total outgoing</td>
				<td>{{round(total())}}€</td>
			</tr>
		</tfoot>
	</table>
	<button @click="changeSort">{{sorting}}</button>
	<button @click="changeReversed">{{reversed ? "up" : "down"}}</button>
</template>

<script>

export default {
	name: "TransactionTable",
	props: {
		data: {},
	},
	data() {
		return {
			idx: 0,
			sorting: "value",
			reversed: false
		}
	},
	methods: {
		total() {
			if (!this.data || this.data == {}) {
				return 0;
			}

			let total = 0;
			for (let val in this.data) {
				total += this.data[val];
			}
			return total;
		},
		round(num) {
			return Math.round(num * 100) / 100;
		},
		index() {
			this.idx++;
			return this.idx - 1;
		},
		getKeys() {
			//let array = []
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
			//console.log(this.sorting)
		},
		changeReversed() {
			this.reversed = !this.reversed;
			//console.log(this.reversed)
		}
	}
}

</script>

<style scoped>

</style>