<template>

<section class="section">
    <div class="tile is-ancestor">
      <div class="tile">
        <div class="tile is-parent is-4">
          <article class="tile is-child">
            <img src="/static/logo-512-pad.png">
          </article>
        </div>

        <div class="tile is-parent">
          <article class="tile is-child">
            <div class="content">
              <p class="title">
                Darkon Demo
              </p>
              <p class="subtitle">
                The showcase of Darkon api
              </p>
              <div class="container">
                <ul>
                  <li v-for="item, idx in demoList" :key="idx">
                    <router-link :to="item[1]"> {{ item[0] }}</router-link>
                  </li>
                </ul>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
</section>
</template>

<script>
import demoList from '../conf.js'

export default {
  name: 'home',

  data () {
    return {
      demoList: demoList()
    }
  }
}
</script>

<style lang="sass" scoped>
@import '../assets/sass/main.scss';

.tile img
  width: 13em

.content
  text-align: left
  padding-top: 2em

</style>
