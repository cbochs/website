<template>
  <div class="home">
    <p>I'm home!</p>
    <form method="post" @submit.prevent="register">
      <input v-model.trim="email"    placeholder="email">
      <input v-model.trim="username" placeholder="username">
      <input v-model.trim="password" placeholder="password" type="password">
      <input type="submit" value="Register">
    </form>
    <div v-if="info">
      <p>{{ info.user_id }}</p>
      <p>{{ info.username }}</p>
      <p>{{ info.email }}</p>
    </div>
    <br>
    <button @click="login">Login</button>
    <br>
    <button @click="logout">Logout</button>
    <br>
    <button @click="currentUser">Get User</button>
    <br>
    <button @click="me">Me!</button>
  </div>
</template>

<script>
import axios from 'axios'
import { getCurrentUser, registerUser, loginUser, logoutUser, spotifyMe } from '@/api'
export default {
  name: 'Home',
  components: {},
  data() {
    return {
      email: null,
      username: null,
      password: null,
      info: null
    }
  },
  methods: {
    register() {
      if (this.email !== null || this.email !== ''
          && this.username !== null || this.username !== ''
          && this.password !== null || this.password !== '') {
        console.log('empty fields when registering')
        return
      }
      
      console.log('registering user')
      registerUser(this.email, this.username, this.password)
        .then(response => console.log(response.status + ' ' + response.data))
        .catch(error => console.log(error.message))
      this.email = ''
      this.username = ''
      this.password = ''
    },
    login() {
      if (this.email !== null || this.email !== ''
          && this.username !== null || this.username !== ''
          && this.password !== null || this.password !== '') {
        console.log('empty fields when logging in')
        return
      }

        console.log('logging user in')
        loginUser(this.email, this.username, this.password)
          .then(response => console.log(response.status + ' ' + response.data))
          .catch(error => console.log(error.message))
        this.email = ''
        this.username = ''
        this.password = ''
    },
    logout() {
      logoutUser()
        .then(response => console.log(response.status + ' ' + response.data))
        .catch(error => console.log(error.message))
    },
    currentUser() {
      getCurrentUser()
        .then(response => response.data)
        .then(data => this.info = data)
    },
    me() {
      spotifyMe()
        .then(response => {
          console.log(response.data)
          if (response.data.auth_url) {
            window.location = response.data.auth_url
          }
        })
        .catch(error => {
          console.log(error.message)
          console.log(error.response.data)
        })
    }
  }
}
</script>
