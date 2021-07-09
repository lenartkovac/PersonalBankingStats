<template>
  <Heading/>
  <Controller/>
</template>

<script>
import Heading from './components/Heading.vue'
import Controller from './components/Controller.vue'

export default {
  name: 'App',
  components: {
    Heading,
    Controller
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>
