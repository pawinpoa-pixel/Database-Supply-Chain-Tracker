<template>
  <div class="dashboard">
    <header>
      <h1>Supply Chain Tracker</h1>
      <div class="header-actions">
        <DarkModeToggle />
        <button class="btn-logout" @click="handleLogout">Logout</button>
      </div>
    </header>

    <nav class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </nav>

    <main>
      <div v-if="activeTab === 'catalog'" class="tab-content stack">
        <ResourcePanel
          title="Categories"
          :fields="categoryFields"
          :list-fn="categories.list"
          :create-fn="categories.create"
          :remove-fn="categories.remove"
        />
        <ResourcePanel
          title="Products"
          :fields="productFields"
          :list-fn="products.list"
          :create-fn="products.create"
          :remove-fn="products.remove"
        />
      </div>

      <div v-if="activeTab === 'partners'" class="tab-content stack">
        <ResourcePanel
          title="Suppliers"
          :fields="supplierFields"
          :list-fn="suppliers.list"
          :create-fn="suppliers.create"
          :remove-fn="suppliers.remove"
        />
        <ResourcePanel
          title="Customers"
          :fields="customerFields"
          :list-fn="customers.list"
          :create-fn="customers.create"
          :remove-fn="customers.remove"
        />
        <ResourcePanel
          title="Carriers"
          :fields="carrierFields"
          :list-fn="carriers.list"
          :create-fn="carriers.create"
          :remove-fn="carriers.remove"
        />
      </div>

      <div v-if="activeTab === 'warehouses'" class="tab-content stack">
        <ResourcePanel
          title="Warehouses"
          :fields="warehouseFields"
          :list-fn="warehouses.list"
          :create-fn="warehouses.create"
          :remove-fn="warehouses.remove"
        />
        <InventoryPanel />
      </div>

      <div v-if="activeTab === 'purchase-orders'" class="tab-content">
        <PurchaseOrdersPanel />
      </div>

      <div v-if="activeTab === 'orders'" class="tab-content">
        <OrdersPanel />
      </div>

      <div v-if="activeTab === 'shipments'" class="tab-content">
        <ShipmentsPanel />
      </div>

      <div v-if="activeTab === 'settings'" class="tab-content">
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
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { logout, changePassword } from '../api/auth'
import { categories, products } from '../api/catalog'
import { suppliers, customers, carriers } from '../api/partners'
import { warehouses } from '../api/warehouses'
import ResourcePanel from '../components/ResourcePanel.vue'
import InventoryPanel from '../components/InventoryPanel.vue'
import PurchaseOrdersPanel from '../components/PurchaseOrdersPanel.vue'
import OrdersPanel from '../components/OrdersPanel.vue'
import ShipmentsPanel from '../components/ShipmentsPanel.vue'
import DarkModeToggle from '../components/DarkModeToggle.vue'

const router = useRouter()

const tabs = [
  { key: 'catalog', label: 'Catalog' },
  { key: 'partners', label: 'Partners' },
  { key: 'warehouses', label: 'Warehouses' },
  { key: 'purchase-orders', label: 'Purchase Orders' },
  { key: 'orders', label: 'Orders' },
  { key: 'shipments', label: 'Shipments' },
  { key: 'settings', label: 'Settings' },
]
const activeTab = ref('catalog')

const categoryFields = [
  { key: 'category_name', label: 'Name', type: 'text', required: true },
  { key: 'description', label: 'Description', type: 'text' },
]

const productFields = [
  { key: 'sku', label: 'SKU', type: 'text', required: true },
  { key: 'product_name', label: 'Name', type: 'text', required: true },
  {
    key: 'category_id',
    label: 'Category',
    type: 'select',
    optionsSource: () => categories.list().then((list) => list.map((c) => ({ value: c.id, label: c.category_name }))),
    display: (row) => row.category?.category_name ?? '',
  },
  { key: 'unit_price', label: 'Unit price', type: 'number', step: '0.01', required: true },
  { key: 'reorder_level', label: 'Reorder level', type: 'number', required: true, default: '0' },
  {
    key: 'is_active',
    label: 'Active',
    type: 'checkbox',
    default: true,
    display: (row) => (row.is_active ? 'Yes' : 'No'),
  },
]

const supplierFields = [
  { key: 'company_name', label: 'Company', type: 'text', required: true },
  { key: 'contact_name', label: 'Contact', type: 'text' },
  { key: 'email', label: 'Email', type: 'text' },
  { key: 'phone', label: 'Phone', type: 'text' },
  { key: 'address', label: 'Address', type: 'text' },
]

const customerFields = [
  { key: 'customer_name', label: 'Name', type: 'text', required: true },
  { key: 'email', label: 'Email', type: 'text' },
  { key: 'phone', label: 'Phone', type: 'text' },
  { key: 'address', label: 'Address', type: 'text' },
]

const carrierFields = [
  { key: 'carrier_name', label: 'Name', type: 'text', required: true },
  { key: 'phone', label: 'Phone', type: 'text' },
  { key: 'email', label: 'Email', type: 'text' },
]

const warehouseFields = [
  { key: 'warehouse_name', label: 'Name', type: 'text', required: true },
  { key: 'address', label: 'Address', type: 'text' },
  { key: 'capacity', label: 'Capacity', type: 'number' },
]

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
  background: var(--color-bg-alt);
  font-family: sans-serif;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--color-surface);
  padding: 1rem 2rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

header h1 {
  font-size: 1.3rem;
  color: var(--color-text);
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-logout {
  padding: 0.45rem 1rem;
  background: var(--color-danger);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
}

.btn-logout:hover {
  background: var(--color-danger-hover);
}

.tabs {
  display: flex;
  gap: 0.5rem;
  padding: 1rem 2rem 0;
  flex-wrap: wrap;
}

.tabs button {
  padding: 0.55rem 1.1rem;
  background: none;
  border: none;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.tabs button.active {
  background: var(--color-surface);
  color: var(--color-primary);
}

main {
  padding: 2rem;
  max-width: 1100px;
}

.tab-content.stack {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.card {
  background: var(--color-surface);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: var(--shadow-card);
  max-width: 480px;
}

h2 {
  font-size: 1.4rem;
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

button[type='submit'] {
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

button[type='submit']:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

button[type='submit']:disabled {
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
</style>
