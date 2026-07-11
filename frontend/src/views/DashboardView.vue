<template>
  <div class="app-shell" :class="{ 'sidebar-open': sidebarOpen }">
    <aside class="sidebar">
      <div class="sidebar-glow" />

      <div class="sidebar-brand">
        <span class="brand-mark">SC</span>
        <span class="brand-name">Supply Chain<br />Tracker</span>
      </div>

      <nav class="sidebar-nav">
        <span class="nav-section-label">Menu</span>
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="nav-item"
          :class="{ active: activeTab === tab.key, 'nav-item-divider': tab.key === 'settings' }"
          @click="selectTab(tab.key)"
        >
          <span class="nav-icon"><component :is="tab.icon" /></span>
          <span class="nav-label">{{ tab.label }}</span>
        </button>
      </nav>
    </aside>

    <div class="sidebar-scrim" @click="sidebarOpen = false" />

    <div class="main-column">
      <header class="topbar">
        <button class="menu-toggle" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle menu">
          <IconMenu />
        </button>

        <div class="breadcrumb">
          <button class="crumb-home" @click="selectTab('catalog')">
            <IconHome />
          </button>
          <span class="crumb-sep">/</span>
          <span class="crumb-current">{{ activeTabLabel }}</span>
        </div>

        <div class="topbar-actions">
          <DarkModeToggle />

          <div class="user-menu">
            <button class="user-chip" @click="userMenuOpen = !userMenuOpen">
              <span class="avatar">{{ userInitial }}</span>
              <span class="username">{{ username || 'Admin' }}</span>
              <IconChevronDown />
            </button>
            <div v-if="userMenuOpen" class="user-dropdown">
              <button @click="goToSettings">
                <IconKey />
                Change password
              </button>
              <button class="logout-item" @click="handleLogout">
                <IconLogout />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main class="content-area">
        <div v-if="activeTab === 'catalog'" class="content-stack">
          <ResourcePanel
            title="Parent Categories"
            :fields="parentCategoryFields"
            :list-fn="categories.list"
            :create-fn="categories.create"
            :update-fn="categories.update"
            :remove-fn="categories.remove"
            :filter="isParentCategory"
          />
          <ResourcePanel
            title="Subcategories"
            :fields="subcategoryFields"
            :list-fn="categories.list"
            :create-fn="categories.create"
            :update-fn="categories.update"
            :remove-fn="categories.remove"
            :filter="isSubcategory"
          />
          <ResourcePanel
            title="Products"
            :fields="productFields"
            :list-fn="products.list"
            :create-fn="products.create"
            :update-fn="products.update"
            :remove-fn="products.remove"
          />
        </div>

        <div v-if="activeTab === 'partners'" class="content-stack">
          <ResourcePanel
            title="Suppliers"
            :fields="supplierFields"
            :list-fn="suppliers.list"
            :create-fn="suppliers.create"
            :update-fn="suppliers.update"
            :remove-fn="suppliers.remove"
          />
          <ResourcePanel
            title="Customers"
            :fields="customerFields"
            :list-fn="customers.list"
            :create-fn="customers.create"
            :update-fn="customers.update"
            :remove-fn="customers.remove"
          />
          <ResourcePanel
            title="Carriers"
            :fields="carrierFields"
            :list-fn="carriers.list"
            :create-fn="carriers.create"
            :update-fn="carriers.update"
            :remove-fn="carriers.remove"
          />
        </div>

        <div v-if="activeTab === 'warehouses'" class="content-stack">
          <ResourcePanel
            title="Warehouses"
            :fields="warehouseFields"
            :list-fn="warehouses.list"
            :create-fn="warehouses.create"
            :update-fn="warehouses.update"
            :remove-fn="warehouses.remove"
          />
          <InventoryPanel />
        </div>

        <div v-if="activeTab === 'purchase-orders'" class="content-stack">
          <PurchaseOrdersPanel />
        </div>

        <div v-if="activeTab === 'orders'" class="content-stack">
          <OrdersPanel />
        </div>

        <div v-if="activeTab === 'shipments'" class="content-stack">
          <ShipmentsPanel />
        </div>

        <div v-if="activeTab === 'settings'" class="content-stack">
          <section class="card settings-card">
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
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { logout, changePassword, getCurrentUsername } from '../api/auth'
import { categories, products } from '../api/catalog'
import { suppliers, customers, carriers } from '../api/partners'
import { warehouses } from '../api/warehouses'
import ResourcePanel from '../components/ResourcePanel.vue'
import InventoryPanel from '../components/InventoryPanel.vue'
import PurchaseOrdersPanel from '../components/PurchaseOrdersPanel.vue'
import OrdersPanel from '../components/OrdersPanel.vue'
import ShipmentsPanel from '../components/ShipmentsPanel.vue'
import DarkModeToggle from '../components/DarkModeToggle.vue'
import IconHome from '../components/icons/IconHome.vue'
import IconGrid from '../components/icons/IconGrid.vue'
import IconUsers from '../components/icons/IconUsers.vue'
import IconWarehouse from '../components/icons/IconWarehouse.vue'
import IconClipboard from '../components/icons/IconClipboard.vue'
import IconPackage from '../components/icons/IconPackage.vue'
import IconTruck from '../components/icons/IconTruck.vue'
import IconSettings from '../components/icons/IconSettings.vue'
import IconLogout from '../components/icons/IconLogout.vue'
import IconChevronDown from '../components/icons/IconChevronDown.vue'
import IconMenu from '../components/icons/IconMenu.vue'
import IconKey from '../components/icons/IconKey.vue'

const router = useRouter()

const tabs = [
  { key: 'catalog', label: 'Catalog', icon: IconGrid },
  { key: 'partners', label: 'Partners', icon: IconUsers },
  { key: 'warehouses', label: 'Warehouses', icon: IconWarehouse },
  { key: 'purchase-orders', label: 'Purchase Orders', icon: IconClipboard },
  { key: 'orders', label: 'Orders', icon: IconPackage },
  { key: 'shipments', label: 'Shipments', icon: IconTruck },
  { key: 'settings', label: 'Settings', icon: IconSettings },
]
const activeTab = ref('catalog')
const activeTabLabel = computed(() => tabs.find((t) => t.key === activeTab.value)?.label ?? '')
const sidebarOpen = ref(false)
const userMenuOpen = ref(false)
const username = getCurrentUsername()
const userInitial = computed(() => (username ? username[0].toUpperCase() : 'A'))

function selectTab(key) {
  activeTab.value = key
  sidebarOpen.value = false
  userMenuOpen.value = false
}

function goToSettings() {
  selectTab('settings')
}

function isParentCategory(row) {
  return !row.parent_category_id
}

function isSubcategory(row) {
  return !!row.parent_category_id
}

const parentCategoryFields = [
  { key: 'category_name', label: 'Name', type: 'text', required: true },
  { key: 'description', label: 'Description', type: 'text', hideInTable: true },
  { key: 'color_hex', label: 'Color', type: 'color', default: '#4361ee' },
]

const subcategoryFields = [
  { key: 'category_name', label: 'Name', type: 'text', required: true },
  { key: 'description', label: 'Description', type: 'text', hideInTable: true },
  {
    key: 'parent_category_id',
    label: 'Parent category',
    type: 'select',
    required: true,
    optionsSource: () =>
      categories.list().then((list) =>
        list.filter(isParentCategory).map((c) => ({ value: c.id, label: c.category_name }))
      ),
    display: (row) => row.parent?.category_name ?? '—',
  },
  { key: 'color_hex', label: 'Color', type: 'color', default: '#4361ee' },
]

const unitOfMeasureOptions = [
  { value: 'EA', label: 'Each (EA)' },
  { value: 'BOX', label: 'Box' },
  { value: 'CASE', label: 'Case' },
  { value: 'PACK', label: 'Pack' },
  { value: 'PALLET', label: 'Pallet' },
  { value: 'KG', label: 'Kilogram (KG)' },
  { value: 'L', label: 'Litre (L)' },
]

const productFields = [
  { key: 'image_url', label: 'Image', type: 'image' },
  { key: 'sku', label: 'SKU', type: 'text', required: true },
  { key: 'product_name', label: 'Name', type: 'text', required: true },
  { key: 'brand', label: 'Brand', type: 'text' },
  { key: 'barcode', label: 'Barcode / UPC', type: 'text', hideInTable: true },
  {
    key: 'category_id',
    label: 'Category',
    type: 'select',
    optionsSource: () => categories.list().then((list) => list.map((c) => ({ value: c.id, label: c.category_name }))),
    display: (row) => row.category?.category_name ?? '—',
  },
  {
    key: 'primary_supplier_id',
    label: 'Primary supplier',
    type: 'select',
    optionsSource: () => suppliers.list().then((list) => list.map((s) => ({ value: s.id, label: s.company_name }))),
    display: (row) => row.primary_supplier?.company_name ?? '—',
  },
  {
    key: 'unit_of_measure',
    label: 'Unit of measure',
    type: 'select',
    default: 'EA',
    optionsSource: () => Promise.resolve(unitOfMeasureOptions),
    display: (row) => row.unit_of_measure ?? 'EA',
  },
  { key: 'unit_price', label: 'Unit price', type: 'number', step: '0.01', required: true },
  { key: 'weight_kg', label: 'Weight (kg)', type: 'number', step: '0.001', hideInTable: true },
  { key: 'reorder_level', label: 'Reorder level', type: 'number', required: true, default: '0' },
  { key: 'max_stock_level', label: 'Max stock', type: 'number' },
  { key: 'description', label: 'Description', type: 'text', hideInTable: true },
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
.app-shell {
  min-height: 100vh;
  display: flex;
  background: var(--color-bg-alt);
}

/* Sidebar */
.sidebar {
  width: 252px;
  flex-shrink: 0;
  background: var(--color-sidebar-bg);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 20;
  overflow: hidden;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.18);
}

.sidebar-glow {
  position: absolute;
  top: -120px;
  left: -80px;
  width: 320px;
  height: 320px;
  background: radial-gradient(circle, rgba(79, 209, 193, 0.22), transparent 70%);
  pointer-events: none;
  z-index: 0;
}

.sidebar-brand {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem 1.35rem;
  margin-bottom: 0.25rem;
}

.brand-mark {
  width: 38px;
  height: 38px;
  border-radius: 11px;
  background: linear-gradient(135deg, var(--color-sidebar-brand), #2fa8a0);
  color: #06231f;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.85rem;
  flex-shrink: 0;
  box-shadow: 0 6px 16px rgba(79, 209, 193, 0.35);
}

.brand-name {
  color: var(--color-sidebar-text-active);
  font-weight: 700;
  font-size: 0.93rem;
  line-height: 1.3;
  letter-spacing: 0.01em;
}

.sidebar-nav {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0.9rem 1rem;
  gap: 0.2rem;
  overflow-y: auto;
}

.nav-section-label {
  color: var(--color-sidebar-text);
  opacity: 0.55;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  padding: 0.5rem 0.6rem 0.4rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.6rem 0.7rem;
  border: none;
  border-radius: 10px;
  background: none;
  color: var(--color-sidebar-text);
  font-size: 0.87rem;
  font-weight: 600;
  cursor: pointer;
  text-align: left;
  transition: background-color 0.18s ease, color 0.18s ease, transform 0.18s ease;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-sidebar-text);
  flex-shrink: 0;
  transition: background-color 0.18s ease, color 0.18s ease;
}

.nav-item:hover {
  background: var(--color-sidebar-hover-bg);
  color: var(--color-sidebar-text-active);
  transform: translateX(2px);
}

.nav-item:hover .nav-icon {
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-sidebar-text-active);
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(79, 209, 193, 0.18), rgba(67, 97, 238, 0.16));
  color: var(--color-sidebar-text-active);
  box-shadow: inset 0 0 0 1px rgba(79, 209, 193, 0.25), 0 4px 14px rgba(0, 0, 0, 0.15);
}

.nav-item.active .nav-icon {
  background: linear-gradient(135deg, var(--color-sidebar-brand), var(--color-sidebar-accent));
  color: #06231f;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.25);
}

.nav-item-divider {
  margin-top: 0.6rem;
  padding-top: 0.9rem;
  position: relative;
}

.nav-item-divider::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0.6rem;
  right: 0.6rem;
  height: 1px;
  background: var(--color-sidebar-border);
}

.sidebar-scrim {
  display: none;
}

/* Main column */
.main-column {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.topbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.85rem 1.75rem;
  background: var(--color-surface);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 10;
}

.menu-toggle {
  display: none;
  border: none;
  background: none;
  color: var(--color-text);
  cursor: pointer;
  padding: 0.3rem;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.crumb-home {
  display: flex;
  border: none;
  background: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0.2rem;
}

.crumb-home:hover {
  color: var(--color-primary);
}

.crumb-sep {
  opacity: 0.6;
}

.crumb-current {
  color: var(--color-text);
  font-weight: 600;
}

.topbar-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-menu {
  position: relative;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.35rem 0.7rem 0.35rem 0.35rem;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: var(--color-surface);
  color: var(--color-text);
  cursor: pointer;
}

.avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  flex-shrink: 0;
}

.username {
  font-size: 0.85rem;
  font-weight: 600;
}

.user-dropdown {
  position: absolute;
  right: 0;
  top: calc(100% + 0.5rem);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  box-shadow: var(--shadow-card);
  min-width: 190px;
  padding: 0.4rem;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.user-dropdown button {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.55rem 0.65rem;
  border: none;
  background: none;
  border-radius: 6px;
  color: var(--color-text);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  text-align: left;
}

.user-dropdown button:hover {
  background: var(--color-surface-hover);
}

.logout-item {
  color: var(--color-danger) !important;
}

.content-area {
  padding: 1.75rem;
  max-width: 1200px;
  width: 100%;
}

.content-stack {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.card {
  background: var(--color-surface);
  border-radius: 14px;
  box-shadow: var(--shadow-card);
  padding: 2rem;
}

.settings-card {
  max-width: 480px;
}

h2 {
  font-size: 1.3rem;
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

/* Responsive */
@media (max-width: 900px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    transform: translateX(-100%);
    transition: transform 0.2s ease;
  }

  .app-shell.sidebar-open .sidebar {
    transform: translateX(0);
  }

  .app-shell.sidebar-open .sidebar-scrim {
    display: block;
    position: fixed;
    inset: 0;
    background: var(--color-overlay);
    z-index: 15;
  }

  .menu-toggle {
    display: inline-flex;
  }

  .username {
    display: none;
  }

  .content-area {
    padding: 1.25rem;
  }
}
</style>
