import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.withCredentials = true

export function getCurrentUser() {
  return axios.get('/api/user')
}

export function registerUser(email, username, password) {
  return axios.post('/api/register', {
    email,
    username,
    password
  })
}

export function loginUser(email, username, password) {
  return axios.post('/api/login', {
    email,
    username,
    password
  })
}

export function logoutUser() {
  return axios.get('/api/logout')
}

export function spotifyAuthorize(params) {
  return axios.get('/api/spotify/authorize', {params})
}

export function spotifyMe() {
  return axios.get('/api/spotify/me')
}
