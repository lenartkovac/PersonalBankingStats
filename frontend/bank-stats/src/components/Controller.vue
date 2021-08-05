<template>
	<div>
		<div class="controller">
			<span class="prev" @click="decMonth"><i class="fas fa-chevron-left"/></span>
			<span>{{months[currentMonth - 1]}} {{currentMonth}}</span>
			<span class="next" @click="incMonth"><i class="fas fa-chevron-right"/></span>
		</div>
		<div class="container">
			<MonthStats v-bind:month="currentMonth" :key="currentMonth"/>
		</div>
	</div>
</template>


<script>
import MonthStats from './MonthStats.vue'
//import { useStore } from 'vuex'
//import { 
//	onMounted, 
//	reactive, 
//	toRefs 
//} from 'vue'

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
			//console.log(this.$state)
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
	-webkit-user-select: none;  /* Chrome all / Safari all */
	-moz-user-select: none;     /* Firefox all */
	-ms-user-select: none;      /* IE 10+ */
}

.prev {
	margin-right: 0.5em
}

.next {
	margin-left: 0.5em
}

.container {
	width: 75%;
	margin-left: 10%;
}

</style>
