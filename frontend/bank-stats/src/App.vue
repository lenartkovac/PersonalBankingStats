<template>
  <Heading/>
  <MonthStats/>
</template>

<script>
import Heading from './components/Heading.vue'
import MonthStats from './components/MonthStats.vue'

export default {
  name: 'App',
  components: {
    Heading,
    MonthStats
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>
