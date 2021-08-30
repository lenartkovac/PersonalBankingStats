<template>
	<span class="select">
		<select v-model="selected">
			<option v-for="catName in catNames" :value="catName" :key="catName" :disabled="catName === currCategory">
				{{catName}}
			</option>
		</select>
		<button @click="select">select</button>
	</span>
</template>

<script>
import { API_URL } from '@/assets/constants'

export default {
	name: "CategorySelect",
	props: {
		currCategory: {
			type: String
		}
	},
	emits: ['selection'],
	data() {
		return {
			catNames: [],
			selected: null
		}
	},
	methods: {
		select() {
			this.$emit('selection', this.selected);
		}
	},
	mounted() {
		this.axios.get(`${API_URL}/categories/names`)
			.then((response) => {
				if (!response 
				|| !response.data 
				|| response.data.status !== "OK" 
				|| !response.data.data) {
					this.error = "Error retrieving data"
				}
				this.catNames = response.data.data
				if (this.catNames.length > 0) {
					this.selected = this.catNames[0];
				}
				if (this.currCategory && this.currCategory == this.selected) {
					this.selected = this.catNames[1];
				}
			})
	}
}

</script>

<style scoped>
.select {
	width: fit-content;
}

</style>