<template>
  <div class="panel">
    <h2>Invoices</h2>
    <p class="hint">
      Bills raised against standing orders — who owes it, what it's for, and how much, itemized by
      product rather than just a lump total.
    </p>

    <table v-if="invoicesList.length" class="data-table">
      <thead>
        <tr>
          <th>Invoice</th>
          <th>Bill To</th>
          <th>Standing Order</th>
          <th>Billing period</th>
          <th>Due</th>
          <th>Total</th>
          <th>Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <template v-for="inv in invoicesList" :key="inv.id">
          <tr>
            <td>#{{ inv.id }}</td>
            <td>{{ inv.customer.customer_name }}</td>
            <td>#{{ inv.standing_order_id }}</td>
            <td>{{ formatDate(inv.billing_period_start) }} – {{ formatDate(inv.billing_period_end) }}</td>
            <td>{{ formatDate(inv.due_date) }}</td>
            <td>${{ inv.total_amount }}</td>
            <td><span class="status" :class="inv.status">{{ inv.status }}</span></td>
            <td class="actions-cell">
              <button v-if="inv.status === 'pending'" class="btn-pay" @click="handlePay(inv)">Mark paid</button>
              <button class="btn-secondary" @click="toggleExpand(inv.id)">
                {{ expanded[inv.id] ? 'Hide items' : 'Show items' }}
              </button>
            </td>
          </tr>
          <tr v-if="expanded[inv.id]">
            <td colspan="8">
              <div class="invoice-detail">
                <p class="detail-label">What's being billed</p>
                <p v-if="!inv.items.length" class="empty">No line items on this invoice.</p>
                <table v-else class="data-table nested">
                  <thead>
                    <tr>
                      <th>SKU</th>
                      <th>Product</th>
                      <th>Qty</th>
                      <th>Unit price</th>
                      <th>Line total</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="line in inv.items" :key="line.id">
                      <td>{{ line.product.sku }}</td>
                      <td>{{ line.product.product_name }}</td>
                      <td>{{ line.quantity }}</td>
                      <td>${{ line.unit_price }}</td>
                      <td>${{ (line.quantity * line.unit_price).toFixed(2) }}</td>
                    </tr>
                  </tbody>
                </table>

                <p class="detail-label">Covers orders</p>
                <p class="order-refs">
                  <span v-for="o in inv.orders" :key="o.id" class="order-ref">#{{ o.id }} ({{ formatDate(o.order_date) }})</span>
                </p>
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
    <p v-else class="empty">No invoices yet — generate one from an active standing order above.</p>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { invoices as invoicesApi } from '../api/invoices'

const invoicesList = ref([])
const expanded = reactive({})
const error = ref('')

function formatDate(value) {
  return value ? new Date(value).toLocaleDateString() : ''
}

function toggleExpand(id) {
  expanded[id] = !expanded[id]
}

async function loadAll() {
  invoicesList.value = await invoicesApi.list()
}

async function handlePay(inv) {
  error.value = ''
  try {
    await invoicesApi.pay(inv.id)
    await loadAll()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to mark invoice as paid.'
  }
}

onMounted(loadAll)
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
  max-width: 60ch;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.data-table th,
.data-table td {
  text-align: left;
  padding: 0.5rem 0.6rem;
  border-bottom: 1px solid var(--color-border-subtle);
}

.data-table th {
  color: var(--color-text-muted);
  font-weight: 600;
  font-size: 0.8rem;
}

.data-table.nested {
  font-size: 0.85rem;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.status {
  display: inline-block;
  padding: 0.1rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--color-primary-tint);
  color: var(--color-primary);
  text-transform: capitalize;
}

.status.paid {
  background: var(--color-success-tint);
  color: var(--color-success);
}

.status.overdue,
.status.cancelled {
  background: var(--color-danger-tint);
  color: var(--color-danger);
}

.invoice-detail {
  padding: 0.75rem 0.5rem 0.25rem;
  background: var(--color-bg-alt);
  border-radius: 8px;
}

.detail-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--color-text-muted);
  margin: 0.75rem 0.25rem 0.4rem;
}

.detail-label:first-child {
  margin-top: 0.1rem;
}

.order-refs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding: 0 0.25rem 0.5rem;
}

.order-ref {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  background: var(--color-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: 6px;
  padding: 0.15rem 0.5rem;
}

.empty {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  padding: 0.5rem 0;
}

button {
  padding: 0.45rem 0.9rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
}

button:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.btn-pay {
  background: var(--color-success);
}

.btn-pay:hover {
  opacity: 0.9;
}

.btn-secondary {
  background: var(--color-primary-tint);
  color: var(--color-primary);
}

.error {
  color: var(--color-danger);
  font-size: 0.85rem;
  margin-top: 0.75rem;
}
</style>
