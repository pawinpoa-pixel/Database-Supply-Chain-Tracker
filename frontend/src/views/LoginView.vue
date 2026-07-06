<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h1>Supply Chain Tracker</h1>
      <h2>Sign In</h2>
      <form @submit.prevent="handleLogin">
        <div class="field">
          <label>Username</label>
          <input v-model="username" type="text" placeholder="Enter username" required />
        </div>
        <div class="field">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="Enter password" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
      <p class="switch">Don't have an account? <router-link to="/register">Register</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api/auth'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await login(username.value, password.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-alt);
}

.auth-card {
  background: var(--color-surface);
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: var(--shadow-card);
  width: 100%;
  max-width: 400px;
}

h1 {
  font-size: 1.2rem;
  color: var(--color-text-muted);
  margin-bottom: 0.25rem;
  font-weight: 500;
}

h2 {
  font-size: 1.8rem;
  color: var(--color-text);
  margin-bottom: 1.5rem;
}

.field {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 0.4rem;
}

input {
  width: 100%;
  padding: 0.65rem 0.85rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 0.95rem;
  box-sizing: border-box;
  background: var(--color-surface);
  color: var(--color-text);
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: var(--color-primary);
}

button {
  width: 100%;
  padding: 0.75rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s;
}

button:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: var(--color-danger);
  font-size: 0.85rem;
  margin: 0.5rem 0;
}

.switch {
  text-align: center;
  margin-top: 1.25rem;
  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.switch a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
}
</style>
