<template>
<div id="app">
  <Navibar />
  <router-view />
  <Footer />
</div>
</template>

<script>
import Navibar from '@/components/Navibar'
import Footer from '@/components/Footer'

export default {
  components: {
    Navibar,
    Footer
  },
  name: 'app',
  data () {
    return {
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /*margin-top: 60px;*/
}
</style>
