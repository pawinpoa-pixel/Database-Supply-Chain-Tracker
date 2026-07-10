<template>
  <div class="panel">
    <h2>Shipments</h2>

    <form class="add-form" @submit.prevent="handleCreateShipment">
      <div class="field">
        <label>Source warehouse</label>
        <select v-model="newShipment.source_warehouse_id" required>
          <option value="" disabled>Select...</option>
          <option v-for="w in warehouses" :key="w.id" :value="w.id">{{ w.warehouse_name }}</option>
        </select>
      </div>
      <div class="field">
        <label>Destination warehouse</label>
        <select v-model="newShipment.destination_warehouse_id" required>
          <option value="" disabled>Select...</option>
          <option v-for="w in warehouses" :key="w.id" :value="w.id">{{ w.warehouse_name }}</option>
        </select>
      </div>
      <div class="field">
        <label>Carrier</label>
        <select v-model="newShipment.carrier_id">
          <option value="">None</option>
          <option v-for="c in carriers" :key="c.id" :value="c.id">{{ c.carrier_name }}</option>
        </select>
      </div>
      <div class="field">
        <label>Tracking number</label>
        <input type="text" v-model="newShipment.tracking_number" />
      </div>
      <p v-if="createError" class="error">{{ createError }}</p>
      <button type="submit" :disabled="creating">{{ creating ? 'Creating...' : 'Create shipment' }}</button>
    </form>

    <div v-for="shipment in shipments" :key="shipment.id" class="order-card">
      <div class="order-header">
        <div>
          <strong>Shipment #{{ shipment.id }}</strong>
          {{ shipment.source_warehouse.warehouse_name }} &rarr; {{ shipment.destination_warehouse ? shipment.destination_warehouse.warehouse_name : 'Customer' }}
          <span class="status" :class="shipment.status">{{ shipment.status }}</span>
        </div>
        <div class="actions">
          <button v-if="shipment.status === 'pending'" class="btn-delete" @click="handleDeleteShipment(shipment.id)">
            Delete
          </button>
        </div>
      </div>

      <table v-if="shipment.items.length" class="data-table">
        <thead>
          <tr>
            <th>SKU</th>
            <th>Product</th>
            <th>Qty</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in shipment.items" :key="item.id">
            <td>{{ item.product.sku }}</td>
            <td>{{ item.product.product_name }}</td>
            <td>{{ item.quantity }}</td>
            <td>
              <button
                v-if="shipment.status === 'pending'"
                class="btn-delete"
                @click="handleRemoveItem(shipment, item.id)"
              >
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No items yet.</p>

      <form v-if="shipment.status === 'pending'" class="add-form" @submit.prevent="handleAddItem(shipment)">
        <div class="field">
          <label>Product</label>
          <select v-model="itemForms[shipment.id].product_id" required>
            <option value="" disabled>Select...</option>
            <option v-for="p in products" :key="p.id" :value="p.id">{{ p.sku }} — {{ p.product_name }}</option>
          </select>
        </div>
        <div class="field">
          <label>Quantity</label>
          <input type="number" min="1" v-model="itemForms[shipment.id].quantity" required />
        </div>
        <button type="submit">Add item</button>
      </form>

      <div class="actions-row">
        <button v-if="shipment.status === 'pending'" @click="handleShip(shipment)">Ship</button>
        <button v-if="shipment.status === 'in_transit'" @click="handleDeliver(shipment)">Deliver</button>
        <button class="btn-secondary" @click="toggleHistory(shipment)">
          {{ historyVisible[shipment.id] ? 'Hide history' : 'Show history' }}
        </button>
      </div>
      <p v-if="actionError[shipment.id]" class="error">{{ actionError[shipment.id] }}</p>

      <ShipmentTimeline
        v-if="historyVisible[shipment.id]"
        :history="history[shipment.id] || []"
      />
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { shipments as shipmentsApi } from '../api/shipments'
import { warehouses as warehousesApi } from '../api/warehouses'
import { carriers as carriersApi } from '../api/partners'
import { products as productsApi } from '../api/catalog'
import ShipmentTimeline from './ShipmentTimeline.vue'

const shipments = ref([])
const warehouses = ref([])
const carriers = ref([])
const products = ref([])

const newShipment = reactive({
  source_warehouse_id: '',
  destination_warehouse_id: '',
  carrier_id: '',
  tracking_number: '',
})
const creating = ref(false)
const createError = ref('')

const itemForms = reactive({})
const actionError = reactive({})
const historyVisible = reactive({})
const history = reactive({})

function ensureFormsFor(shipment) {
  if (!itemForms[shipment.id]) itemForms[shipment.id] = { product_id: '', quantity: '' }
}

function formatDate(value) {
  return value ? new Date(value).toLocaleString() : ''
}

async function loadAll() {
  shipments.value = await shipmentsApi.list()
  shipments.value.forEach(ensureFormsFor)
}

async function handleCreateShipment() {
  createError.value = ''
  creating.value = true
  try {
    await shipmentsApi.create({
      source_warehouse_id: Number(newShipment.source_warehouse_id),
      destination_warehouse_id: Number(newShipment.destination_warehouse_id),
      carrier_id: newShipment.carrier_id ? Number(newShipment.carrier_id) : null,
      tracking_number: newShipment.tracking_number || null,
      items: [],
    })
    newShipment.source_warehouse_id = ''
    newShipment.destination_warehouse_id = ''
    newShipment.carrier_id = ''
    newShipment.tracking_number = ''
    await loadAll()
  } catch (err) {
    createError.value = err.response?.data?.detail || 'Failed to create shipment.'
  } finally {
    creating.value = false
  }
}

async function handleDeleteShipment(id) {
  await shipmentsApi.remove(id)
  await loadAll()
}

async function handleAddItem(shipment) {
  actionError[shipment.id] = ''
  const form = itemForms[shipment.id]
  try {
    await shipmentsApi.addItem(shipment.id, {
      product_id: Number(form.product_id),
      quantity: Number(form.quantity),
    })
    await loadAll()
  } catch (err) {
    actionError[shipment.id] = err.response?.data?.detail || 'Failed to add item.'
  }
}

async function handleRemoveItem(shipment, itemId) {
  await shipmentsApi.removeItem(shipment.id, itemId)
  await loadAll()
}

async function handleShip(shipment) {
  actionError[shipment.id] = ''
  try {
    await shipmentsApi.ship(shipment.id)
    await loadAll()
  } catch (err) {
    actionError[shipment.id] = err.response?.data?.detail || 'Failed to ship.'
  }
}

async function handleDeliver(shipment) {
  actionError[shipment.id] = ''
  try {
    await shipmentsApi.deliver(shipment.id)
    await loadAll()
  } catch (err) {
    actionError[shipment.id] = err.response?.data?.detail || 'Failed to deliver.'
  }
}

async function toggleHistory(shipment) {
  historyVisible[shipment.id] = !historyVisible[shipment.id]
  if (historyVisible[shipment.id]) {
    history[shipment.id] = await shipmentsApi.history(shipment.id)
  }
}

onMounted(async () => {
  const [shipmentList, warehouseList, carrierList, productList] = await Promise.all([
    shipmentsApi.list(),
    warehousesApi.list(),
    carriersApi.list(),
    productsApi.list(),
  ])
  warehouses.value = warehouseList
  carriers.value = carrierList
  products.value = productList
  shipments.value = shipmentList
  shipments.value.forEach(ensureFormsFor)
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

.status.delivered {
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

.btn-secondary {
  background: var(--color-primary-tint);
  color: var(--color-primary);
}

.actions-row {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.history {
  margin-top: 0.75rem;
  padding-left: 1.2rem;
  font-size: 0.85rem;
  color: var(--color-text);
}

.error {
  color: var(--color-danger);
  font-size: 0.85rem;
  width: 100%;
  margin-top: 0.4rem;
}
</style>
