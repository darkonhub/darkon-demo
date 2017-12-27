<template>
<nav class="navbar">
  <div class="navbar-brand">
    <a class="navbar-item" href="http://localhost:8080">
      <img src="/static/logo-h.png" alt="Darkon Demo" height="28">
    </a>
    <div class="navbar-burger burger" data-target="navbarExampleTransparentExample" @click="showNav = !showNav" :class="{'is-active': showNav}">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>

  <div id="navbarExampleTransparentExample" class="navbar-menu" :class="{'is-active': showNav}">
    <div class="navbar-start">
      <a class="navbar-item" href="http://localhost:8080">
        Home
      </a>
      <a class="navbar-item" href="http://darkon.io">
        Doc
      </a>
      <div class="navbar-item has-dropdown is-hoverable">
        <router-link to="/overview" class="navbar-link">
          Demo
        </router-link>
        <div class="navbar-dropdown is-boxed">
          <router-link to="/influence" class="navbar-item">
            Upweighting Influence
          </router-link>
        </div>
      </div>
    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="field is-grouped">
          <p class="control">
            <a class="bd-tw-button button" data-social-network="Twitter" data-social-action="tweet" data-social-target="http://localhost:4000" target="_blank" href="https://twitter.com/intent/tweet?text=Bulma: a modern CSS framework based on Flexbox&amp;hashtags=bulmaio&amp;url=http://localhost:4000&amp;via=jgthms">
              <span class="icon">
                <i class="fa fa-twitter"></i>
              </span>
              <span>
                Tweet
              </span>
            </a>
          </p>
          <p class="control">
            <a class="button is-primary" href="#">
              <span class="icon">
                <i class="fa fa-download"></i>
              </span>
              <span>Download</span>
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</nav>
</template>

<script>
export default {
  data () {
    return {
      showNav: false
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
