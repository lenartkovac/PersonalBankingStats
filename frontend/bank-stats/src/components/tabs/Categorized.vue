<template>
	<h5>{{title}} for month {{month}}</h5>
</template>

<script>
export default {
	props: {
		month: {
			type: Number,
			default: 0
		}
	},
	data () {
		return {
			title: "Categorized"
		}
	}
}
</script>

<style scoped>

</style>