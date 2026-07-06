<template>
  <div class="panel">
    <h2>Orders</h2>

    <form class="add-form" @submit.prevent="handleCreateOrder">
      <div class="field">
        <label>Customer</label>
        <select v-model="newOrder.customer_id" required>
          <option value="" disabled>Select...</option>
          <option v-for="c in customers" :key="c.id" :value="c.id">{{ c.customer_name }}</option>
        </select>
      </div>
      <p v-if="createError" class="error">{{ createError }}</p>
      <button type="submit" :disabled="creating">{{ creating ? 'Creating...' : 'Create order' }}</button>
    </form>

    <div v-for="order in orders" :key="order.id" class="order-card">
      <div class="order-header">
        <div>
          <strong>Order #{{ order.id }}</strong> — {{ order.customer.customer_name }}
          <span class="status" :class="order.status">{{ order.status }}</span>
          <span class="total">${{ order.total_amount }}</span>
        </div>
        <div class="actions">
          <button v-if="order.status === 'pending'" class="btn-delete" @click="handleDeleteOrder(order.id)">
            Delete
          </button>
        </div>
      </div>

      <table v-if="order.items.length" class="data-table">
        <thead>
          <tr>
            <th>SKU</th>
            <th>Product</th>
            <th>Qty</th>
            <th>Selling price</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in order.items" :key="item.id">
            <td>{{ item.product.sku }}</td>
            <td>{{ item.product.product_name }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.selling_price }}</td>
            <td>
              <button
                v-if="order.status === 'pending'"
                class="btn-delete"
                @click="handleRemoveItem(order, item.id)"
              >
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No items yet.</p>

      <form v-if="order.status === 'pending'" class="add-form" @submit.prevent="handleAddItem(order)">
        <div class="field">
          <label>Product</label>
          <select v-model="itemForms[order.id].product_id" required>
            <option value="" disabled>Select...</option>
            <option v-for="p in products" :key="p.id" :value="p.id">{{ p.sku }} — {{ p.product_name }}</option>
          </select>
        </div>
        <div class="field">
          <label>Quantity</label>
          <input type="number" min="1" v-model="itemForms[order.id].quantity" required />
        </div>
        <div class="field">
          <label>Selling price</label>
          <input type="number" step="0.01" min="0" v-model="itemForms[order.id].selling_price" required />
        </div>
        <button type="submit">Add item</button>
      </form>

      <form v-if="order.status === 'pending'" class="add-form" @submit.prevent="handleFulfill(order)">
        <div class="field">
          <label>Fulfill from warehouse</label>
          <select v-model="fulfillWarehouse[order.id]" required>
            <option value="" disabled>Select...</option>
            <option v-for="w in warehouses" :key="w.id" :value="w.id">{{ w.warehouse_name }}</option>
          </select>
        </div>
        <button type="submit" class="btn-primary">Fulfill</button>
      </form>
      <p v-if="actionError[order.id]" class="error">{{ actionError[order.id] }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { orders as ordersApi } from '../api/orders'
import { customers as customersApi } from '../api/partners'
import { products as productsApi } from '../api/catalog'
import { warehouses as warehousesApi } from '../api/warehouses'

const orders = ref([])
const customers = ref([])
const products = ref([])
const warehouses = ref([])

const newOrder = reactive({ customer_id: '' })
const creating = ref(false)
const createError = ref('')

const itemForms = reactive({})
const fulfillWarehouse = reactive({})
const actionError = reactive({})

function ensureFormsFor(order) {
  if (!itemForms[order.id]) itemForms[order.id] = { product_id: '', quantity: '', selling_price: '' }
  if (!(order.id in fulfillWarehouse)) fulfillWarehouse[order.id] = ''
}

async function loadAll() {
  orders.value = await ordersApi.list()
  orders.value.forEach(ensureFormsFor)
}

async function handleCreateOrder() {
  createError.value = ''
  creating.value = true
  try {
    await ordersApi.create({ customer_id: Number(newOrder.customer_id), items: [] })
    newOrder.customer_id = ''
    await loadAll()
  } catch (err) {
    createError.value = err.response?.data?.detail || 'Failed to create order.'
  } finally {
    creating.value = false
  }
}

async function handleDeleteOrder(id) {
  await ordersApi.remove(id)
  await loadAll()
}

async function handleAddItem(order) {
  actionError[order.id] = ''
  const form = itemForms[order.id]
  try {
    await ordersApi.addItem(order.id, {
      product_id: Number(form.product_id),
      quantity: Number(form.quantity),
      selling_price: Number(form.selling_price),
    })
    await loadAll()
  } catch (err) {
    actionError[order.id] = err.response?.data?.detail || 'Failed to add item.'
  }
}

async function handleRemoveItem(order, itemId) {
  await ordersApi.removeItem(order.id, itemId)
  await loadAll()
}

async function handleFulfill(order) {
  actionError[order.id] = ''
  try {
    await ordersApi.fulfill(order.id, Number(fulfillWarehouse[order.id]))
    await loadAll()
  } catch (err) {
    actionError[order.id] = err.response?.data?.detail || 'Failed to fulfill order.'
  }
}

onMounted(async () => {
  const [orderList, customerList, productList, warehouseList] = await Promise.all([
    ordersApi.list(),
    customersApi.list(),
    productsApi.list(),
    warehousesApi.list(),
  ])
  customers.value = customerList
  products.value = productList
  warehouses.value = warehouseList
  orders.value = orderList
  orders.value.forEach(ensureFormsFor)
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
  margin-bottom: 1.25rem;
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
  margin-bottom: 0.75rem;
}

.total {
  margin-left: 0.6rem;
  color: var(--color-text-muted);
  font-size: 0.9rem;
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

.status.received,
.status.delivered,
.status.fulfilled {
  background: var(--color-success-tint);
  color: var(--color-success);
}

.status.cancelled {
  background: var(--color-danger-tint);
  color: var(--color-danger);
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

.error {
  color: var(--color-danger);
  font-size: 0.85rem;
  width: 100%;
  margin-top: 0.4rem;
}
</style>
