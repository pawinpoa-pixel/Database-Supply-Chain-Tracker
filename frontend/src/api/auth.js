import { api } from './client'

export async function login(username, password) {
  const { data } = await api.post('/auth/login', { username, password })
  localStorage.setItem('token', data.access_token)
  return data
}

export async function register(username, email, password) {
  const { data } = await api.post('/auth/register', { username, email, password })
  return data
}

export async function changePassword(currentPassword, newPassword) {
  const { data } = await api.put('/auth/change-password', {
    current_password: currentPassword,
    new_password: newPassword,
  })
  return data
}

export function logout() {
  localStorage.removeItem('token')
}

export function getToken() {
  return localStorage.getItem('token')
}
