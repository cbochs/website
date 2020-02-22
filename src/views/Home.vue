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
  </div>
</template>

<script>
import { getCurrentUser, registerUser, loginUser, logoutUser } from '@/api'
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
      if (this.email !== null && this.email !== ''
          && this.username !== null && this.username !== ''
          && this.password !== null && this.password !== '')
        return
      
      console.log('registering user')
      registerUser(this.email, this.username, this.password)
        .then(response => console.log(response.status))
        .catch(error => console.log(error.message))
      this.email = ''
      this.username = ''
      this.password = ''
    },
    login() {
      if (this.email !== null && this.email !== ''
          && this.username !== null && this.username !== ''
          && this.password !== null && this.password !== '')
        return

        console.log('logging user in')
        loginUser(this.email, this.username, this.password)
          .then(response => console.log(response.status))
          .catch(error => console.log(error.message))
        this.email = ''
        this.username = ''
        this.password = ''
    },
    logout() {
      logoutUser()
        .then(response => console.log(response.status))
        .catch(error => console.log(error.message))
    },
    currentUser() {
      getCurrentUser()
        .then(response => response.data)
        .then(data => this.info = data)
    }
  }
}
</script>
