<template>
	<div>
		<Tabs>
			<Tab title="Incoming">
				<Incoming/>
			</Tab>
			<Tab title="Outgoing">
				<Outgoing/>
			</Tab>
			<Tab title="Categorized">
				<Categorized/>
			</Tab>
		</Tabs>
	</div>
</template>

<script>
import Tabs from './Tabs.vue'
import Tab from './Tab.vue'
import Incoming from './tabs/Incoming.vue'
import Outgoing from './tabs/Outgoing.vue'
import Categorized from './tabs/Categorized.vue'

export default {
	components: {
		Tabs,
		Tab,
		Incoming,
		Outgoing,
		Categorized
	}
}
</script>

<style>
.container {
	border: 1px;
	border-style: solid;
	border-color: black;
	border-radius: 1em;
	box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}

</style>