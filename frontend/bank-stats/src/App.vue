<template>
  <div>
    <Heading/>
    <router-view/>
  </div>
</template>

<script>
import Heading from './components/Heading.vue'

export default {
  name: 'App',
  components: {
    Heading
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>