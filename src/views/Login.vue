<template>
  <v-card width="400" class="mx-auto mt-5">
    <v-card-title>
      <h1 class="display-1">Login</h1>
      <v-spacer></v-spacer>
      <v-btn text to="/">Home</v-btn>
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field
          v-model="username"
          label="Username"
          prepend-icon="mdi-account-circle"
          required
        />

        <v-text-field
          v-model="password"
          label="Password"
          prepend-icon="mdi-lock"
          :type="showPassword ? 'text' : 'password'"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="showPassword = !showPassword"
          required
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="indigo" to="/register">Register</v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="login" color="info">Login</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'Login',
  components: {},
  data() {
    return {
      showPassword: false,
      username: null,
      password: null
    }
  },
  computed: {},
  methods: {
    login() {

    }
  }
}
</script>
