import Vue from 'vue'
import Router from 'vue-router'
// import Home from '@/views/Home'
import Influence from '@/views/Influence'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Influence
    },
    {
      path: '/influence',
      name: 'Influence',
      component: Influence
    }
  ]
})
