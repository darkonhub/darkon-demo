import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Influence from '@/views/Influence'
import GradcamImage from '@/views/GradcamImage'
import GradcamText from '@/views/GradcamText'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/influence',
      name: 'Influence',
      component: Influence
    },
    {
      path: '/gradcam-image',
      name: 'GradcamImage',
      component: GradcamImage
    },
    {
      path: '/gradcam-text',
      name: 'GradcamText',
      component: GradcamText
    }
  ]
})
