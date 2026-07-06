<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h1>Supply Chain Tracker</h1>
      <h2>Create Account</h2>
      <form @submit.prevent="handleRegister">
        <div class="field">
          <label>Username</label>
          <input v-model="username" type="text" placeholder="Choose a username" required />
        </div>
        <div class="field">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="Enter your email" required />
        </div>
        <div class="field">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="Create a password" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="success" class="success">{{ success }}</p>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
      </form>
      <p class="switch">Already have an account? <router-link to="/login">Sign In</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../api/auth'

const router = useRouter()
const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await register(username.value, email.value, password.value)
    success.value = 'Account created! Redirecting to login...'
    setTimeout(() => router.push('/login'), 1500)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed. Please try again.'
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

.success {
  color: var(--color-success);
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
