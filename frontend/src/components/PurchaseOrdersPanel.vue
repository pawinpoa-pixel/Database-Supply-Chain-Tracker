<template>
  <div class="panel">
    <h2>Purchase Orders</h2>

    <form class="add-form" @submit.prevent="handleCreatePO">
      <div class="field">
        <label>Supplier</label>
        <select v-model="newPO.supplier_id" required>
          <option value="" disabled>Select...</option>
          <option v-for="s in suppliers" :key="s.id" :value="s.id">{{ s.company_name }}</option>
        </select>
      </div>
      <div class="field">
        <label>Expected delivery</label>
        <input type="date" v-model="newPO.expected_delivery_date" />
      </div>
      <p v-if="createError" class="error">{{ createError }}</p>
      <button type="submit" :disabled="creating">{{ creating ? 'Creating...' : 'Create PO' }}</button>
    </form>

    <div v-for="po in purchaseOrders" :key="po.id" class="order-card">
      <div class="order-header">
        <div>
          <strong>PO #{{ po.id }}</strong> — {{ po.supplier.company_name }}
          <span class="status" :class="po.status">{{ po.status }}</span>
        </div>
        <div class="actions">
          <button v-if="po.status === 'pending'" class="btn-delete" @click="handleDeletePO(po.id)">Delete</button>
        </div>
      </div>

      <table v-if="po.items.length" class="data-table">
        <thead>
          <tr>
            <th>SKU</th>
            <th>Product</th>
            <th>Qty</th>
            <th>Unit cost</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in po.items" :key="item.id">
            <td>{{ item.product.sku }}</td>
            <td>{{ item.product.product_name }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.unit_cost }}</td>
            <td>
              <button v-if="po.status === 'pending'" class="btn-delete" @click="handleRemoveItem(po, item.id)">
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No items yet.</p>

      <form v-if="po.status === 'pending'" class="add-form" @submit.prevent="handleAddItem(po)">
        <div class="field">
          <label>Product</label>
          <select v-model="itemForms[po.id].product_id" required>
            <option value="" disabled>Select...</option>
            <option v-for="p in products" :key="p.id" :value="p.id">{{ p.sku }} — {{ p.product_name }}</option>
          </select>
        </div>
        <div class="field">
          <label>Quantity</label>
          <input type="number" min="1" v-model="itemForms[po.id].quantity" required />
        </div>
        <div class="field">
          <label>Unit cost</label>
          <input type="number" step="0.01" min="0" v-model="itemForms[po.id].unit_cost" required />
        </div>
        <button type="submit">Add item</button>
      </form>

      <form v-if="po.status === 'pending'" class="add-form" @submit.prevent="handleReceive(po)">
        <div class="field">
          <label>Receive into warehouse</label>
          <select v-model="receiveWarehouse[po.id]" required>
            <option value="" disabled>Select...</option>
            <option v-for="w in warehouses" :key="w.id" :value="w.id">{{ w.warehouse_name }}</option>
          </select>
        </div>
        <button type="submit" class="btn-primary">Receive</button>
      </form>
      <p v-if="actionError[po.id]" class="error">{{ actionError[po.id] }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { purchaseOrders as poApi } from '../api/purchaseOrders'
import { suppliers as suppliersApi } from '../api/partners'
import { products as productsApi } from '../api/catalog'
import { warehouses as warehousesApi } from '../api/warehouses'

const purchaseOrders = ref([])
const suppliers = ref([])
const products = ref([])
const warehouses = ref([])

const newPO = reactive({ supplier_id: '', expected_delivery_date: '' })
const creating = ref(false)
const createError = ref('')

const itemForms = reactive({})
const receiveWarehouse = reactive({})
const actionError = reactive({})

function ensureFormsFor(po) {
  if (!itemForms[po.id]) itemForms[po.id] = { product_id: '', quantity: '', unit_cost: '' }
  if (!(po.id in receiveWarehouse)) receiveWarehouse[po.id] = ''
}

async function loadAll() {
  purchaseOrders.value = await poApi.list()
  purchaseOrders.value.forEach(ensureFormsFor)
}

async function handleCreatePO() {
  createError.value = ''
  creating.value = true
  try {
    await poApi.create({
      supplier_id: Number(newPO.supplier_id),
      expected_delivery_date: newPO.expected_delivery_date || null,
      items: [],
    })
    newPO.supplier_id = ''
    newPO.expected_delivery_date = ''
    await loadAll()
  } catch (err) {
    createError.value = err.response?.data?.detail || 'Failed to create purchase order.'
  } finally {
    creating.value = false
  }
}

async function handleDeletePO(id) {
  await poApi.remove(id)
  await loadAll()
}

async function handleAddItem(po) {
  actionError[po.id] = ''
  const form = itemForms[po.id]
  try {
    await poApi.addItem(po.id, {
      product_id: Number(form.product_id),
      quantity: Number(form.quantity),
      unit_cost: Number(form.unit_cost),
    })
    await loadAll()
  } catch (err) {
    actionError[po.id] = err.response?.data?.detail || 'Failed to add item.'
  }
}

async function handleRemoveItem(po, itemId) {
  await poApi.removeItem(po.id, itemId)
  await loadAll()
}

async function handleReceive(po) {
  actionError[po.id] = ''
  try {
    await poApi.receive(po.id, Number(receiveWarehouse[po.id]))
    await loadAll()
  } catch (err) {
    actionError[po.id] = err.response?.data?.detail || 'Failed to receive purchase order.'
  }
}

onMounted(async () => {
  const [poList, supplierList, productList, warehouseList] = await Promise.all([
    poApi.list(),
    suppliersApi.list(),
    productsApi.list(),
    warehousesApi.list(),
  ])
  suppliers.value = supplierList
  products.value = productList
  warehouses.value = warehouseList
  purchaseOrders.value = poList
  purchaseOrders.value.forEach(ensureFormsFor)
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
