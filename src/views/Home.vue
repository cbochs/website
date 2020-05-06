<template>
  <v-card width="450" class="mx-auto mt-5">
    <v-card-title>
      <h1 class="display-1">imsignificant!</h1>
    </v-card-title>
    <v-card-actions>
      <v-btn to="/register">Register</v-btn>
      <v-btn to="/login">Login</v-btn>
      <v-btn>Authorize (Spotify)</v-btn>
    </v-card-actions>
    <v-card-content>
      <v-container>
        <v-autocomplete
          v-model="selectedTags"
          :items="availableTags"
          multiple chips small-chips
          label="Search"
          clearable deletable-chips
        ></v-autocomplete>
      </v-container>
    </v-card-content>
  </v-card>
</template>

<script>
export default {
  name: 'Home',
  components: {},
  data() {
    return {
      selectedTags: [],
      availableTags: ['discover', 'happy', 'sad']
    }
  },
  methods: {}
}
</script>
