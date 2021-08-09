<template>
	<div class="heading">
			<span class="logo">
				<img src="../assets/logo.png"/>
			</span>
		<div class="title">
			<span >Bank meme</span>
			<span class="router">
				<span v-if="path === '/settings'">
					<router-link to="/"><i class="fas fa-home"/></router-link>
				</span>
				<span v-else>
					<router-link to="/settings"><i class="fas fa-cog"/></router-link>
				</span>
			</span>
		</div>
	</div>
</template>

<script>
import { useRoute } from 'vue-router'
import { computed } from 'vue'

export default {
	name: "Heading",
	setup() {
		const route = useRoute()
		
		const path = computed(() => route.path)
		return {path}
	}
}
</script>

<style scoped>
.heading {
	padding: 1em;
	background: red;
	/*
	box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
	box-shadow: 2/0px 0 0 0 gray;
	box-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px;
	*/
	box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
}

img {
	float: left;
	width: 2.5em;
}

.title {
	/*
	margin: 0.5em 0 1em 1em;
	*/
	font-size: 1.5em;
}

.router {
	float: right;
}

.router:link {
	color: black;
}

</style>