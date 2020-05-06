import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import { spotifyAuthorize } from '@/api'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/lazy',
    name: 'Lazy',
    component: () => import('../views/Lazy.vue')
  },
  {
    path: '/authorize',
    name: 'SpotifyAuth',
    beforeEnter(to, from, next) {
      spotifyAuthorize(to.query)
        .then(response => console.log(response.status + ' ' + response.data))
        .catch(error => console.log(error.message))
      next(from)
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
