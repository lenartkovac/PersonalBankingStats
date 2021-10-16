<template>
	<div class="heading">
			<span class="logo">
				<img clas="logo" src="@/assets/logo.svg"/>
			</span>
		<div class="title">
			<span >Bank Stats</span>
			<div class="router">
				<span v-if="path === '/settings'">
					<router-link class="routerLink" to="/"><i class="fas fa-home"/></router-link>
				</span>
				<span v-else>
					<router-link class="routerLink" to="/settings"><i class="fas fa-cog"/></router-link>
				</span>
			</div>
		</div>
	</div>
</template>

<script>
import { useRoute } from 'vue-router';
import { computed } from 'vue';

export default {
	name: 'Heading',
	setup() {
		const route = useRoute();
		
		const path = computed(() => route.path);
		return {path};
	}
};
</script>

<style scoped>
.heading {
	padding: 1em;
	background: red;
	box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
}

img {
	float: left;
	height: 30px;
	margin-right: 1em;
}

.title {
	/*
	margin: 0.5em 0 1em 1em;
	*/
	font-size: 1.5em;
}

.router {
	float: right;
	display: inline;
}

.routerLink {
	color: black;
}

</style>