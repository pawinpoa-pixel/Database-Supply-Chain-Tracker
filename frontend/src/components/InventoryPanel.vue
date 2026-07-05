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
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 1.5rem 2rem 2rem;
}

h2 {
  font-size: 1.3rem;
  color: #1a1a2e;
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
  border-bottom: 1px solid #eee;
}

.data-table th {
  color: #555;
  font-weight: 600;
  font-size: 0.8rem;
}

tr.low {
  background: #fdecea;
}

.badge {
  background: #e63946;
  color: white;
  border-radius: 6px;
  padding: 0.1rem 0.4rem;
  font-size: 0.7rem;
  font-weight: 600;
  margin-left: 0.3rem;
}

.empty {
  color: #666;
  font-size: 0.9rem;
}
</style>
