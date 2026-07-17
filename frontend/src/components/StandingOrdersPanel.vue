<template>
  <div class="panel">
    <h2>Standing Orders</h2>
    <p class="hint">
      A standing order is a customer's agreement for periodic deliveries of set products — it
      releases a real order every delivery cycle, but bills for those releases separately on its
      own cycle (e.g. deliver weekly, bill monthly).
    </p>

    <form class="add-form" @submit.prevent="handleCreateStandingOrder">
      <div class="field">
        <label>Customer</label>
        <select v-model="newStandingOrder.customer_id" required>
          <option value="" disabled>Select...</option>
          <option v-for="c in customers" :key="c.id" :value="c.id">{{ c.customer_name }}</option>
        </select>
      </div>
      <div class="field">
        <label>Deliver every (days)</label>
        <input type="number" min="1" v-model="newStandingOrder.delivery_frequency_days" required />
      </div>
      <div class="field">
        <label>Bill every (days)</label>
        <input type="number" min="1" v-model="newStandingOrder.billing_frequency_days" required />
      </div>
      <div class="field">
        <label>Start date</label>
        <input type="date" v-model="newStandingOrder.start_date" required />
      </div>
      <p v-if="createError" class="error">{{ createError }}</p>
      <button type="submit" :disabled="creating">{{ creating ? 'Creating...' : 'Create standing order' }}</button>
    </form>

    <div v-for="so in standingOrdersList" :key="so.id" class="order-card">
      <div class="order-header">
        <div>
          <strong>Standing Order #{{ so.id }}</strong> — {{ so.customer.customer_name }}
          <span class="status" :class="so.status">{{ so.status }}</span>
        </div>
        <div class="actions">
          <button class="btn-delete" @click="handleDeleteStandingOrder(so.id)">Delete</button>
        </div>
      </div>

      <p class="so-meta">
        Delivers every {{ so.delivery_frequency_days }} day(s) — next release on
        {{ formatDate(so.next_delivery_date) }}. Bills every {{ so.billing_frequency_days }} day(s) — next
        invoice on {{ formatDate(so.next_billing_date) }}.
      </p>

      <table v-if="so.items.length" class="data-table">
        <thead>
          <tr>
            <th>SKU</th>
            <th>Product</th>
            <th>Qty / delivery</th>
            <th>Unit price</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in so.items" :key="item.id">
            <td>{{ item.product.sku }}</td>
            <td>{{ item.product.product_name }}</td>
            <td>{{ item.quantity_per_delivery }}</td>
            <td>{{ item.unit_price }}</td>
            <td>
              <button
                v-if="so.status !== 'cancelled'"
                class="btn-delete"
                @click="handleRemoveItem(so, item.id)"
              >
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No agreed products yet.</p>

      <form v-if="so.status !== 'cancelled'" class="add-form" @submit.prevent="handleAddItem(so)">
        <div class="field">
          <label>Product</label>
          <select v-model="itemForms[so.id].product_id" required>
            <option value="" disabled>Select...</option>
            <option v-for="p in products" :key="p.id" :value="p.id">{{ p.sku }} — {{ p.product_name }}</option>
          </select>
        </div>
        <div class="field">
          <label>Qty per delivery</label>
          <input type="number" min="1" v-model="itemForms[so.id].quantity_per_delivery" required />
        </div>
        <div class="field">
          <label>Unit price</label>
          <input type="number" step="0.01" min="0" v-model="itemForms[so.id].unit_price" required />
        </div>
        <button type="submit">Add product</button>
      </form>

      <div class="actions-row">
        <button v-if="so.status === 'active'" @click="handleReleaseOrder(so)">Release next order</button>
        <button class="btn-secondary" @click="handleGenerateInvoice(so)">Generate invoice</button>
        <button v-if="so.status === 'active'" class="btn-secondary" @click="handleSetStatus(so, 'paused')">
          Pause
        </button>
        <button v-if="so.status === 'paused'" class="btn-secondary" @click="handleSetStatus(so, 'active')">
          Resume
        </button>
        <button v-if="so.status !== 'cancelled'" class="btn-delete" @click="handleSetStatus(so, 'cancelled')">
          Cancel
        </button>
      </div>
      <p v-if="actionError[so.id]" class="error">{{ actionError[so.id] }}</p>
      <p v-if="actionSuccess[so.id]" class="success">{{ actionSuccess[so.id] }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { standingOrders as standingOrdersApi } from '../api/standingOrders'
import { customers as customersApi } from '../api/partners'
import { products as productsApi } from '../api/catalog'

const standingOrdersList = ref([])
const customers = ref([])
const products = ref([])

const newStandingOrder = reactive({
  customer_id: '',
  delivery_frequency_days: 7,
  billing_frequency_days: 30,
  start_date: '',
})
const creating = ref(false)
const createError = ref('')

const itemForms = reactive({})
const actionError = reactive({})
const actionSuccess = reactive({})

function ensureFormsFor(so) {
  if (!itemForms[so.id]) itemForms[so.id] = { product_id: '', quantity_per_delivery: '', unit_price: '' }
}

function formatDate(value) {
  return value ? new Date(value).toLocaleDateString() : ''
}

async function loadAll() {
  standingOrdersList.value = await standingOrdersApi.list()
  standingOrdersList.value.forEach(ensureFormsFor)
}

async function handleCreateStandingOrder() {
  createError.value = ''
  creating.value = true
  try {
    await standingOrdersApi.create({
      customer_id: Number(newStandingOrder.customer_id),
      delivery_frequency_days: Number(newStandingOrder.delivery_frequency_days),
      billing_frequency_days: Number(newStandingOrder.billing_frequency_days),
      start_date: newStandingOrder.start_date,
      items: [],
    })
    newStandingOrder.customer_id = ''
    newStandingOrder.delivery_frequency_days = 7
    newStandingOrder.billing_frequency_days = 30
    newStandingOrder.start_date = ''
    await loadAll()
  } catch (err) {
    createError.value = err.response?.data?.detail || 'Failed to create standing order.'
  } finally {
    creating.value = false
  }
}

async function handleDeleteStandingOrder(id) {
  actionError[id] = ''
  try {
    await standingOrdersApi.remove(id)
    await loadAll()
  } catch (err) {
    actionError[id] = err.response?.data?.detail || 'Failed to delete standing order.'
  }
}

async function handleAddItem(so) {
  actionError[so.id] = ''
  const form = itemForms[so.id]
  try {
    await standingOrdersApi.addItem(so.id, {
      product_id: Number(form.product_id),
      quantity_per_delivery: Number(form.quantity_per_delivery),
      unit_price: Number(form.unit_price),
    })
    await loadAll()
  } catch (err) {
    actionError[so.id] = err.response?.data?.detail || 'Failed to add product.'
  }
}

async function handleRemoveItem(so, itemId) {
  actionError[so.id] = ''
  try {
    await standingOrdersApi.removeItem(so.id, itemId)
    await loadAll()
  } catch (err) {
    actionError[so.id] = err.response?.data?.detail || 'Failed to remove product.'
  }
}

async function handleReleaseOrder(so) {
  actionError[so.id] = ''
  actionSuccess[so.id] = ''
  try {
    const order = await standingOrdersApi.releaseOrder(so.id)
    actionSuccess[so.id] = `Order #${order.id} released — view it in the Orders tab.`
    await loadAll()
  } catch (err) {
    actionError[so.id] = err.response?.data?.detail || 'Failed to release order.'
  }
}

async function handleGenerateInvoice(so) {
  actionError[so.id] = ''
  actionSuccess[so.id] = ''
  try {
    const invoice = await standingOrdersApi.generateInvoice(so.id)
    actionSuccess[so.id] = `Invoice #${invoice.id} generated for $${invoice.total_amount} — see it below.`
    await loadAll()
  } catch (err) {
    actionError[so.id] = err.response?.data?.detail || 'Failed to generate invoice.'
  }
}

async function handleSetStatus(so, newStatus) {
  actionError[so.id] = ''
  try {
    await standingOrdersApi.update(so.id, { status: newStatus })
    await loadAll()
  } catch (err) {
    actionError[so.id] = err.response?.data?.detail || 'Failed to update standing order.'
  }
}

onMounted(async () => {
  const [soList, customerList, productList] = await Promise.all([
    standingOrdersApi.list(),
    customersApi.list(),
    productsApi.list(),
  ])
  customers.value = customerList
  products.value = productList
  standingOrdersList.value = soList
  standingOrdersList.value.forEach(ensureFormsFor)
})
</script>

<style scoped>
.panel {
  background: var(--color-surface);
  border-radius: 12px;
  box-shadow: var(--shadow-card);
  padding: 1.5rem 2rem 2rem;
}

h2 {
  font-size: 1.3rem;
  color: var(--color-text);
  margin-bottom: 0.5rem;
}

.hint {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  margin-bottom: 1.25rem;
  max-width: 65ch;
}

.order-card {
  border: 1px solid var(--color-border-subtle);
  border-radius: 10px;
  padding: 1rem 1.25rem;
  margin-top: 1.25rem;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.so-meta {
  font-size: 0.82rem;
  color: var(--color-text-muted);
  margin-bottom: 0.75rem;
}

.status {
  display: inline-block;
  margin-left: 0.6rem;
  padding: 0.1rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--color-primary-tint);
  color: var(--color-primary);
  text-transform: capitalize;
}

.status.paused {
  background: var(--color-danger-tint);
  color: var(--color-danger);
}

.status.cancelled {
  background: var(--color-border-subtle);
  color: var(--color-text-subtle);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
}

.data-table th,
.data-table td {
  text-align: left;
  padding: 0.4rem 0.5rem;
  border-bottom: 1px solid var(--color-border-subtle);
}

.data-table th {
  color: var(--color-text-muted);
  font-weight: 600;
  font-size: 0.8rem;
}

.empty {
  color: var(--color-text-muted);
  font-size: 0.85rem;
  margin-bottom: 0.75rem;
}

.add-form {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: flex-end;
  margin-top: 0.75rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.field label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-text);
}

.field input,
.field select {
  padding: 0.5rem 0.65rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 0.9rem;
  background: var(--color-surface);
  color: var(--color-text);
}

.field input:focus,
.field select:focus {
  outline: none;
  border-color: var(--color-primary);
}

button {
  padding: 0.55rem 1.2rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  height: fit-content;
}

button:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-delete {
  background: none;
  color: var(--color-danger);
  padding: 0;
  font-size: 0.85rem;
}

.btn-secondary {
  background: var(--color-primary-tint);
  color: var(--color-primary);
}

.actions-row {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.75rem;
  flex-wrap: wrap;
}

.error {
  color: var(--color-danger);
  font-size: 0.85rem;
  width: 100%;
  margin-top: 0.4rem;
}

.success {
  color: var(--color-success);
  font-size: 0.85rem;
  width: 100%;
  margin-top: 0.4rem;
}
</style>
