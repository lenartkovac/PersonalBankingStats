<template>
	<div class="tab" v-if="isActive">
		<slot></slot>
	</div>
</template>


<script>
import {
	ref, 
	watch, 
	inject, 
	onBeforeMount
} from "vue"

export default {
	name: "Tab",
	props: {
		title: {
			type: String,
			default: "TAB"
		}
	},
	setup(props) {
		const isActive = ref(false);
		const tabs = inject("TabsProvider");

		watch(
			() => tabs.selectedTab,
			() => {
				isActive.value = props.title === tabs.selectedTab;
			}
		);

		onBeforeMount(() => {
			isActive.value = props.title === tabs.selectedIndex;
		})
		return { isActive };
	}
}
</script>

<style scoped>
</style>