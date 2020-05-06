<template>
  <v-card width="450" class="mx-auto mt-5">
    <v-card-title>
      <h1 class="display-1">New Account</h1>
      <v-spacer></v-spacer>
      <v-btn text to="/">Home</v-btn>
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field
          v-model="username"
          label="Username"
          required
        />

        <v-text-field
          v-model="email"
          label="Email"
          required
        />

        <v-text-field
          v-model="password"
          label="Password"
          :type="showPassword ? 'text' : 'password'"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="showPassword = !showPassword"
          required
        />

        <v-text-field
          v-model="confirmedPassword"
          label="Confirm password"
          :type="showPassword ? 'text' : 'password'"
          required
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn to="/login">Back to login</v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="register" color="info">Register</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  components: {},
  data() {
    return {
      showPassword: false,
      username: null,
      email: null,
      password: null,
      confirmedPassword: null
    }
  },
  computed: {},
  methods: {
    register() {
      console.log('registering...')
      if (this.username === null || this.username === '') return
      if (this.email    === null || this.email === '') return
      if (this.password === null || this.password === '') return
      if (this.confirmedPassword !== this.password) return
      axios.post('http://localhost:5000/register', {
        username: this.username,
        email: this.email,
        password: this.password
      })
      .then(response => console.log(`${response.status} ${response.data}`))
      .catch(error => console.log(`${error.message} ${error.response.data}`))
    }
  }
}
</script>
