<template>
	<div>
		<div class="controller noSelect">
			<span class="prev" @click="decMonth"><i class="fas fa-chevron-left"/></span>
			<span>{{months[currentMonth - 1]}}</span>
			<span class="next" @click="incMonth"><i class="fas fa-chevron-right"/></span>
		</div>
		<div class="container">
			<MonthStats v-bind:month="currentMonth" :key="currentMonth"/>
		</div>
	</div>
</template>


<script>
import MonthStats from '@/components/layout/MonthStats.vue'
import '@/assets/style.css'

export default {
	name: "Controller",
	components: {
		MonthStats
	},
	data() {
		return {
			currentMonth: 2,
			months: [
				"January",
				"February",
				"March",
				"April",
				"May",
				"June",
				"July",
				"August",
				"September",
				"October",
				"November",
				"December"
			]
		}
	},
	methods: {
		incMonth() {
			this.currentMonth = this.currentMonth == 12 ? 1 : this.currentMonth + 1;
			this.$store.commit('changeMonth', this.currentMonth)
		},
		decMonth() {
			this.currentMonth = this.currentMonth ==  1 ? 12 : this.currentMonth - 1;
			this.$store.commit('changeMonth', this.currentMonth)
		}
	},
	mounted() {
		this.currentMonth = this.$store.getters.getCurrMonth
	}
}

</script>

<style scoped>

.controller {
	text-align: center;
	font-size: 3em;
}

.prev {
	margin-right: 0.5em
}

.next {
	margin-left: 0.5em
}


</style>
