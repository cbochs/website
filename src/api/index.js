import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.withCredentials = true

export function getCurrentUser() {
  return axios.get('/api/user')
}

export function registerUser(email, username, password) {
  return axios.post('/register', {
    email,
    username,
    password
  })
}

export function loginUser(email, username, password) {
  return axios.post('/login', {
    email,
    username,
    password
  })
}

export function logoutUser() {
  return axios.get('/logout')
}

export function spotifyAuthorize(params) {
  return axios.get('/spotify/authorize', {params})
}

export function spotifyMe() {
  return axios.get('/spotify/me')
}

export function spotifyPlaylists() {
  return axios.get('/spotify/playlists')
}
