<template>
  <div class="home">
    <p>I'm home!</p>
    <p>{{ output }}</p>
    <form method="post" @submit.prevent="register">
      <input v-model.trim="email"    placeholder="email">
      <input v-model.trim="username" placeholder="username">
      <input v-model.trim="password" placeholder="password" type="password">
      <input type="submit" value="Register">
    </form>
    <p v-if="user">{{ user.username }}</p>
    <p v-if="spotify_user">{{ spotify_user.id }}</p>
    <br>
    <button @click="login">Login</button>
    <button @click="logout">Logout</button>
    <button @click="currentUser">Get User</button>
    <button @click="me">Me!</button>
    <button @click="myPlaylists">My Playlists</button>
    <div v-if="playlists" align="left">
      <ul>
        <li v-for="playlist in playlists" :key="playlist.id">
          Name: {{ playlist.name }}, Tracks: {{ playlist.tracks.total }}, URI: {{ playlist.uri }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { getCurrentUser, registerUser, loginUser, logoutUser, spotifyMe, spotifyPlaylists } from '@/api'
export default {
  name: 'Home',
  components: {},
  data() {
    return {
      email: null,
      username: null,
      password: null,
      user: null,
      spotify_user: null,
      playlists: null,
      output: ''
    }
  },
  methods: {
    register() {
      if (this.email === null || this.email === ''
          || this.username === null || this.username === ''
          || this.password === null || this.password === '') {
        this.output = 'empty fields when registering'
        console.log('empty fields when registering')
        return
      }
      
      console.log('registering user')
      registerUser(this.email, this.username, this.password)
        .then(response => console.log(response.status + ' ' + response.data))
        .catch(error => this.output = error.message + ' ' + error.response.data)
      this.email = ''
      this.username = ''
      this.password = ''
      this.output = 'registered user'
    },
    login() {
      if (this.email === null || this.email === ''
          || this.username === null || this.username === ''
          || this.password === null || this.password === '') {
        this.output = 'empty fields when logging in'
        console.log('empty fields when logging in')
        return
      }

        console.log('logging user in')
        loginUser(this.email, this.username, this.password)
          .then(response => console.log(response.status + ' ' + response.data))
          .catch(error => this.output = error.message + ' ' + error.response.data)
        this.email = ''
        this.username = ''
        this.password = ''
        this.output = 'logged in!'
    },
    logout() {
      logoutUser()
        .then(response => console.log(response.status + ' ' + response.data))
        .catch(error => this.output = error.message + ' ' + error.response.data)
      this.user = null
      this.output = 'logged out'
    },
    currentUser() {
      getCurrentUser()
        .then(response => this.user = response.data)
        .catch(error => this.output = error.message + ' ' + error.response.data)
    },
    me() {
      spotifyMe()
        .then(response => {
          if (response.data.auth_url) {
            window.location = response.data.auth_url
          } else {
            this.spotify_user = response.data
          }
        })
        .catch(error => this.output = error.message + ' ' + error.response.data)
    },
    myPlaylists() {
      spotifyPlaylists()
        .then(response => {
          if (response.data.auth_url) {
            window.location = response.data.auth_url
          } else {
            this.playlists = response.data
            this.output = `found ${this.playlists.length} playlists`
          }
        })
        .catch(error => this.output = error.message + ' ' + error.response.data)
    }
  }
}
</script>
