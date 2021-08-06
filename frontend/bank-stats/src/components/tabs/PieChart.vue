<template>
	<div>
		<canvas id="chart" width="100%" height="70%"></canvas>
	</div>
</template>

<script>
//import { Pie } from 'vue-chartjs'
import Chart from 'chart.js/auto'

export default {
	name: "PieChart",
	//extends: Pie,
	props: {
		month: {
			type: Number
		}
	},
	data() {
		return {
			data: null
		}
	},
	methods: {
		hashCode(catString) {
			return catString.split("")
				.reduce((a, b) => {
					a = ((a << 5) - a) + b.charCodeAt(0);
					return a&a;
				}, 0)
		},
		colorFromString(catName) {
			const hash = this.hashCode(catName)
			const r = (hash & 0xFF0000) >> 16
			const g = (hash & 0x00FF00) >> 8
			const b = (hash & 0x0000FF)

			return [r, g, b]
		},
		showChart() {
			const labels = Object.keys(this.data).filter(label => Object.keys(this.data[label]).length !== 0)
			const dataPoints = labels.map(label => Object.values(this.data[label]).reduce((o1, o2) => o1 + o2))
			const colors = labels.map(label => this.colorFromString(label))
			const backgroundColors = colors.map(color => `rgba(${color[0]}, ${color[1]}, ${color[2]}, 0.6)`)
			const borderColors = colors.map(color => `rgba(${color[0]}, ${color[1]}, ${color[2]}, 1)`)

			const myChart = new Chart('chart', {
				type: 'pie',
				data: {
					labels: labels,
					datasets: [{
						label: "euro",
						data: dataPoints,
						backgroundColor: backgroundColors,
						borderColor: borderColors,
						borderWidth: 1
					}]
				}
			})
			//! not always necessary, but vue compiler will throw error:
			//! "'myChart' is assigned a value but never used"
			myChart.draw()
		}
	},
	mounted() {
		this.axios.get(`http://localhost:5000/api/v1/transactions/${this.month}/outgoing/categorized`)
			.then(response => {
				if (!response 
				|| !response.data 
				|| response.data.status !== "OK" 
				|| !response.data.data) {
					this.error = "Error retrieving data"
				}
				this.data = response.data.data
				this.showChart()
			})
			.catch(error => {
				console.error("error: ", error)
			})
	}
}
</script>

<style scoped>

</style>