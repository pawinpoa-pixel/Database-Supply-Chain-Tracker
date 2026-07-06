<template>
  <div class="panel">
    <h2>Inventory</h2>

    <table v-if="rows.length" class="data-table">
      <thead>
        <tr>
          <th>Warehouse</th>
          <th>SKU</th>
          <th>Product</th>
          <th>Qty on hand</th>
          <th>Reorder level</th>
          <th>Last updated</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.id" :class="{ low: isLow(row) }">
          <td>{{ row.warehouse.warehouse_name }}</td>
          <td>{{ row.product.sku }}</td>
          <td>{{ row.product.product_name }}</td>
          <td>{{ row.quantity_on_hand }} <span v-if="isLow(row)" class="badge">low stock</span></td>
          <td>{{ row.product.reorder_level }}</td>
          <td>{{ formatDate(row.last_updated) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else class="empty">No inventory yet — receive a purchase order to stock a warehouse.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { inventory } from '../api/warehouses'

const rows = ref([])

function isLow(row) {
  return row.quantity_on_hand <= row.product.reorder_level
}

function formatDate(value) {
  return value ? new Date(value).toLocaleString() : ''
}

onMounted(async () => {
  rows.value = await inventory.list()
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

tr.low {
  background: var(--color-danger-tint);
}

.badge {
  background: var(--color-danger);
  color: white;
  border-radius: 6px;
  padding: 0.1rem 0.4rem;
  font-size: 0.7rem;
  font-weight: 600;
  margin-left: 0.3rem;
}

.empty {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}
</style>
