<template>
	<div class="controller">
		<span @click="decMonth"><i class="fas fa-chevron-left"/></span>
		<span>{{currentMonth}}</span>
		<span @click="incMonth"><i class="fas fa-chevron-right"/></span>
	</div>
	<div class="container">
		<MonthStats v-bind:month="currentMonth" :key="currentMonth"/>
	</div>
</template>


<script>
import MonthStats from './MonthStats.vue'

export default {
	name: "Controller",
	components: {
		MonthStats
	},
	data() {
		return {
			currentMonth: 1
		}
	},
	methods: {
		incMonth() {
			this.currentMonth = this.currentMonth == 12 ? 1 : this.currentMonth + 1;
		},
		decMonth() {
			this.currentMonth = this.currentMonth ==  1 ? 12 : this.currentMonth - 1;
		}
	}
}

</script>

<style scoped>
.controller {
	text-align: center;
	font-size: 3em;
}

.container {
	width: 75%;
	margin-left: 10%;
}

.controller span {
	margin-right: 2em
}

</style>
