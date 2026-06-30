import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export async function login(username, password) {
  const { data } = await api.post('/auth/login', { username, password })
  localStorage.setItem('token', data.access_token)
  return data
}

export async function register(username, email, password) {
  const { data } = await api.post('/auth/register', { username, email, password })
  return data
}

export function logout() {
  localStorage.removeItem('token')
}

export function getToken() {
  return localStorage.getItem('token')
}
