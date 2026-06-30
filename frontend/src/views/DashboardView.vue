<template>
  <div class="dashboard">
    <header>
      <h1>Supply Chain Tracker</h1>
      <button @click="handleLogout">Logout</button>
    </header>
    <main>
      <p>Welcome! You are logged in.</p>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { logout } from '../api/auth'

const router = useRouter()

function handleLogout() {
  logout()
  router.push('/login')
}
</script>

<style scoped>
.dashboard {
  font-family: sans-serif;
  padding: 2rem;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
  margin-bottom: 2rem;
}

button {
  padding: 0.5rem 1rem;
  background: #e63946;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}
</style>
