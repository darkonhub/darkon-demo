<template>

<section class="hero-img is-fullheight">
  <div class="hero-body">
    <div class="container">
      <h1 class="title">
        Full Height title
      </h1>
      <h2 class="subtitle">
        Full Height subtitle
      </h2>
    </div>
  </div>
</section>
</template>

<script>
export default {
  name: 'home'
}
</script>

<style lang="sass">
@import '../assets/sass/main.scss';

.hero-img
  @extend .hero
  /*background: no-repeat center url("/static/logo-full.png")*/
  /*background-size: contain*/


</style>
