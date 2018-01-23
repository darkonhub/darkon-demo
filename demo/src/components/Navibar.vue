<template>
<nav class="navbar">
  <div class="navbar-brand">
    <router-link to="/" class="navbar-item">
      <img src="/static/logo-h.png" alt="Darkon Demo" height="28">
    </router-link>
    <div class="navbar-burger burger" data-target="navbarExampleTransparentExample" @click="showNav = !showNav" :class="{'is-active': showNav}">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>

  <div id="navbarExampleTransparentExample" class="navbar-menu" :class="{'is-active': showNav}">
    <div class="navbar-start">
      <!--<a class="navbar-item" href="http://localhost:8080">-->
        <!--Home-->
      <!--</a>-->
      <div class="navbar-item has-dropdown is-hoverable">
        <a @click="route('/')" class="navbar-link">Demo</a>
        <div class="navbar-dropdown is-boxed">
          <a v-for="item, idx in demoList" class="navbar-item" :key="idx" @click="route(item[1])">
            {{ item[0] }}
          </a>
        </div>
      </div>
      <a class="navbar-item" href="http://darkon.io">
        Doc
      </a>
      <a class="navbar-item" href="https://github.com/darkonhub/darkon/">
        Github
      </a>
    </div>

    <div class="navbar-end">
      <!--<div class="navbar-item">-->
        <!--<div class="field is-grouped">-->
          <!--<p class="control">-->
            <!--<a class="bd-tw-button button" data-social-network="Twitter" data-social-action="tweet" data-social-target="http://localhost:4000" target="_blank" href="https://twitter.com/intent/tweet?text=Bulma: a modern CSS framework based on Flexbox&amp;hashtags=bulmaio&amp;url=http://localhost:4000&amp;via=jgthms">-->
              <!--<span class="icon">-->
                <!--<i class="fa fa-twitter"></i>-->
              <!--</span>-->
              <!--<span>-->
                <!--Tweet-->
              <!--</span>-->
            <!--</a>-->
          <!--</p>-->
          <!--<p class="control">-->
            <!--<a class="button is-primary" href="#">-->
              <!--<span class="icon">-->
                <!--<i class="fa fa-download"></i>-->
              <!--</span>-->
              <!--<span>Download</span>-->
            <!--</a>-->
          <!--</p>-->
        <!--</div>-->
      <!--</div>-->
    </div>
  </div>
</nav>
</template>

<script>
import demoList from '../conf.js'

export default {
  data () {
    return {
      showNav: false,
      demoList: demoList()
    }
  },

  methods: {
    route (location) {
      this.showNav = false
      this.$router.push(location)
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../assets/sass/main";

.navbar {
  @include touch {
    .navbar-menu {
      background-color: $primary;
    }
  }
}
</style>
