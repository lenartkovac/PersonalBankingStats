<template>
	<div>
		<div v-if="dataError">
			<Error :message="dataError" @reload="handleReload"/>
		</div>
		<div v-else>
			<canvas id="chart" width="100%" height="70%"></canvas>
		</div>
	</div>
</template>

<script>
import Chart from 'chart.js/auto';
import { API_URL } from '@/assets/constants';
import '@/assets/style.css';
import Error from '@/components/reusables/Error';

export default {
	name: 'PieChart',
	components: {
		Error
	},
	props: {
		date: {
			type: Object 
		}
	},
	data() {
		return {
			data: null,
			dataError: ''
		};
	},
	methods: {
		hashCode(catString) {
			return catString.split('')
				.reduce((a, b) => {
					a = ((a << 5) - a) + b.charCodeAt(0);
					return a&a;
				}, 0);
		},
		colorFromString(catName) {
			const hash = this.hashCode(catName);
			const r = (hash & 0xFF0000) >> 16;
			const g = (hash & 0x00FF00) >> 8;
			const b = (hash & 0x0000FF);

			return [r, g, b];
		},
		showChart() {
			const labels = Object.keys(this.data).filter(label => Object.keys(this.data[label]).length !== 0);
			const dataPoints = labels.map(label => Object.values(this.data[label]).reduce((o1, o2) => o1 + o2));
			const colors = labels.map(label => this.colorFromString(label));
			const backgroundColors = colors.map(color => `rgba(${color[0]}, ${color[1]}, ${color[2]}, 0.6)`);
			const borderColors = colors.map(color => `rgba(${color[0]}, ${color[1]}, ${color[2]}, 1)`);

			const myChart = new Chart('chart', {
				type: 'pie',
				data: {
					labels: labels,
					datasets: [{
						label: 'euro',
						data: dataPoints,
						backgroundColor: backgroundColors,
						borderColor: borderColors,
						borderWidth: 1
					}]
				}
			});
			//! not always necessary, but vue compiler will throw error:
			//! "'myChart' is assigned a value but never used"
			myChart.draw();
		},
		loadData() {
			this.axios.get(`${API_URL}/transactions/${this.date.getFullYear()}/${this.date.getMonth() + 1}/outgoing/categorized`)
				.then(response => {
					if (!response 
					|| !response.data 
					|| response.data.status !== 'OK' 
					|| !response.data.data) {
						this.error = 'Error retrieving data';
					}
					this.data = response.data.data;
					this.showChart();
				})
				.catch(error => {
					if (error.response && error.response.data && error.response.data.error) {
						this.dataError = error.response.data.error;
						return;
					}
					this.dataError = error.message;
				});
		},
		handleReload() {
			this.dataError = '',
			this.loadData();
		}
	},
	mounted() {
		this.loadData();
	}
};
</script>

<style scoped>

</style>