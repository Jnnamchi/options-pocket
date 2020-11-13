<template>
  <div id="app">
    <StockCharter msg="OPTIONS POCKET"/>
  </div>
</template>

<script>
import StockCharter from './components/StockCharter.vue'


export default {
  name: 'App',
  components: {
    StockCharter
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
