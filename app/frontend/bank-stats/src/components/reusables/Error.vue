<template>
	<div class="error">
		<div class="errmsg">
			<span>{{message}}</span>
		</div>
		<div class="reloadIcon" @click="$emit('reload')">
			<i class="fas fa-sync"/>
		</div>

		<div class="reloadText">
			<span>reload page</span>
		</div>
	</div>
</template>

<script>


export default {
	name: 'Error',
	emits: ['reload'],
	props: {
		message: {
			type: String,
			default: 'An error occured'
		}
	}
};

</script>

<style scoped>

.error {
	background: rgba(255, 0, 0, 0.6);
	padding: 0.2em 2em;
	margin-top: 0.3em;
	border-radius: 1em;
	text-align: center;
}

.errmsg {
	margin-bottom: 1em;
}
</style>
