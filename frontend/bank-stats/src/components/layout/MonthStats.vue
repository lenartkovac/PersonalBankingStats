<template>
	<div>
		<Tabs>
			<Tab title="Incoming">
				<Incoming v-bind:month="month" />
			</Tab>
			<Tab title="Outgoing">
				<Outgoing v-bind:month="month" />
			</Tab>
			<Tab title="Categorized">
				<Categorized v-bind:month="month" />
			</Tab>
			<Tab title="Chart">
				<PieChart v-bind:month="month" />
			</Tab>
		</Tabs>
	</div>
</template>

<script>
import Categorized from '@/components/tabs/Categorized.vue'
import Incoming from '@/components/tabs/Incoming.vue'
import Outgoing from '@/components/tabs/Outgoing.vue'
import PieChart from '@/components/tabs/PieChart.vue'
import Tab from '@/components/reusables/Tab.vue'
import Tabs from '@/components/layout/Tabs.vue'

export default {
	components: {
		Tabs,
		Tab,
		Incoming,
		Outgoing,
		Categorized,
		PieChart
	},
	props: {
		month: {
			type: Number,
			default: 1
		}
	}
}
</script>