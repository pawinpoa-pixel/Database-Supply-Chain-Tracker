<template>
  <div class="dashboard">
    <header>
      <h1>Supply Chain Tracker</h1>
      <button class="btn-logout" @click="handleLogout">Logout</button>
    </header>

    <main>
      <section class="card">
        <h2>Change Password</h2>
        <form @submit.prevent="handleChangePassword">
          <div class="field">
            <label>Current Password</label>
            <input v-model="currentPassword" type="password" placeholder="Enter current password" required />
          </div>
          <div class="field">
            <label>New Password</label>
            <input v-model="newPassword" type="password" placeholder="Enter new password" required />
          </div>
          <div class="field">
            <label>Confirm New Password</label>
            <input v-model="confirmPassword" type="password" placeholder="Confirm new password" required />
          </div>
          <p v-if="error" class="error">{{ error }}</p>
          <p v-if="success" class="success">{{ success }}</p>
          <button type="submit" :disabled="loading">
            {{ loading ? 'Updating...' : 'Update Password' }}
          </button>
        </form>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { logout, changePassword } from '../api/auth'

const router = useRouter()

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

function handleLogout() {
  logout()
  router.push('/login')
}

async function handleChangePassword() {
  error.value = ''
  success.value = ''

  if (newPassword.value !== confirmPassword.value) {
    error.value = 'New passwords do not match.'
    return
  }

  loading.value = true
  try {
    await changePassword(currentPassword.value, newPassword.value)
    success.value = 'Password updated successfully!'
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to update password.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f0f2f5;
  font-family: sans-serif;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

header h1 {
  font-size: 1.3rem;
  color: #1a1a2e;
  margin: 0;
}

.btn-logout {
  padding: 0.45rem 1rem;
  background: #e63946;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
}

.btn-logout:hover {
  background: #c1121f;
}

main {
  padding: 2rem;
  max-width: 480px;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

h2 {
  font-size: 1.4rem;
  color: #1a1a2e;
  margin-bottom: 1.5rem;
}

.field {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #444;
  margin-bottom: 0.4rem;
}

input {
  width: 100%;
  padding: 0.65rem 0.85rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #4361ee;
}

button[type='submit'] {
  width: 100%;
  padding: 0.75rem;
  background: #4361ee;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s;
}

button[type='submit']:hover:not(:disabled) {
  background: #3451d1;
}

button[type='submit']:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #e63946;
  font-size: 0.85rem;
  margin: 0.5rem 0;
}

.success {
  color: #2a9d8f;
  font-size: 0.85rem;
  margin: 0.5rem 0;
}
</style>
