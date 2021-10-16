<template>
	<div>
		<Tabs>
			<Tab title="Incoming">
				<Incoming :date="date" />
			</Tab>
			<Tab title="Outgoing">
				<Outgoing :date="date" />
			</Tab>
			<Tab title="Categorized">
				<Categorized :date="date" />
			</Tab>
			<Tab title="Chart">
				<PieChart :date="date" />
			</Tab>
		</Tabs>
	</div>
</template>

<script>
import Categorized from '@/components/tabs/Categorized.vue';
import Incoming from '@/components/tabs/Incoming.vue';
import Outgoing from '@/components/tabs/Outgoing.vue';
import PieChart from '@/components/tabs/PieChart.vue';
import Tab from '@/components/reusables/Tab.vue';
import Tabs from '@/components/layout/Tabs.vue';

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
		date: {
			type: Object
		}
	}
};
</script>