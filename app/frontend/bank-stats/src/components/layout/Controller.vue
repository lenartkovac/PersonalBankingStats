<template>
	<div>
		<div class="controller noSelect">
			<span class="month-mobile">{{months[date.getMonth()]}}</span>
			<span class="prev" title="previous year" @click="changeDate(0, -1)"><i class="fas fa-angle-double-left"/></span>
			<span class="prev" title="previous month" @click="changeDate(-1, 0)"><i class="fas fa-chevron-left"/></span>
			<span class="date">
				<span class="month-desktop">{{months[date.getMonth()]}}</span>
				<span>{{date.getFullYear()}}</span>
			</span>
			<span class="next" title="next month" v-if="!maxMonth" @click="changeDate(1, 0)"><i class="fas fa-chevron-right"/></span>
			<span class="next" title="next year" v-if="!maxYear"  @click="changeDate(0, 1)"><i class="fas fa-angle-double-right"/></span>
		</div>
		<div class="container">
			<MonthStats :date="date" :key="date"/>
		</div>
	</div>
</template>


<script>
import MonthStats from '@/components/layout/MonthStats.vue';
import '@/assets/style.css';
import { mapState } from 'vuex';

export default {
	name: 'Controller',
	components: {
		MonthStats
	},
	data() {
		return {
			months: [
				'January',
				'February',
				'March',
				'April',
				'May',
				'June',
				'July',
				'August',
				'September',
				'October',
				'November',
				'December'
			]
		};
	},
	methods: {
		changeDate(monthDiff, yearDiff) {
			this.$store.dispatch('changeDate', {monthDiff, yearDiff});
		}
	},
	computed: {
		maxYear: function() {
			return this.date.getFullYear() == new Date().getFullYear();
		},
		maxMonth: function() {
			return this.maxYear && this.date.getMonth() == new Date().getMonth();
		},
		...mapState(['date'])
	}
};

</script>

<style scoped>

.controller {
	text-align: center;
	font-size: 3em;
}

.prev {
	margin-right: 0.5em;
}

.next {
	margin-left: 0.5em;
}

.date {
	text-align: center;
	display: inline-block;
	width: 30%;
}

@media only screen and (max-device-width: 1230px) {
	.month-mobile {
		display: block;
	}
	.month-desktop {
		display: none;
	}
}

@media only screen and (min-device-width: 1231px) {
	.month-mobile {
		display: none;
	}
	.month-desktop {
		display: inline-block;
		margin-right: 0.4em;
	}
}

</style>
