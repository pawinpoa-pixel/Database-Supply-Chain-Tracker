<template>
  <div class="panel">
    <h2>{{ title }}</h2>

    <table v-if="rows.length" class="data-table">
      <thead>
        <tr>
          <th v-for="f in fields" :key="f.key">{{ f.label }}</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.id">
          <td v-for="f in fields" :key="f.key">{{ displayValue(row, f) }}</td>
          <td><button class="btn-delete" @click="handleDelete(row.id)">Delete</button></td>
        </tr>
      </tbody>
    </table>
    <p v-else class="empty">No records yet.</p>

    <form class="add-form" @submit.prevent="handleCreate">
      <div class="field" v-for="f in fields" :key="f.key">
        <label>{{ f.label }}</label>
        <select v-if="f.type === 'select'" v-model="form[f.key]" :required="f.required">
          <option value="" disabled>Select...</option>
          <option v-for="opt in optionsCache[f.key] || []" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
        <input v-else-if="f.type === 'checkbox'" type="checkbox" v-model="form[f.key]" />
        <input
          v-else
          :type="f.type"
          :step="f.step"
          v-model="form[f.key]"
          :required="f.required"
        />
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <button type="submit" :disabled="submitting">{{ submitting ? 'Adding...' : 'Add' }}</button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'

const props = defineProps({
  title: { type: String, required: true },
  fields: { type: Array, required: true },
  listFn: { type: Function, required: true },
  createFn: { type: Function, required: true },
  removeFn: { type: Function, required: true },
})

const rows = ref([])
const form = reactive({})
const optionsCache = reactive({})
const error = ref('')
const submitting = ref(false)

function defaultFor(f) {
  if (f.default !== undefined) return f.default
  return f.type === 'checkbox' ? true : ''
}

function resetForm() {
  for (const f of props.fields) form[f.key] = defaultFor(f)
}

function displayValue(row, f) {
  if (f.display) return f.display(row)
  return row[f.key]
}

async function loadRows() {
  rows.value = await props.listFn()
}

async function loadOptions() {
  for (const f of props.fields) {
    if (f.optionsSource) optionsCache[f.key] = await f.optionsSource()
  }
}

async function handleCreate() {
  error.value = ''
  submitting.value = true
  try {
    const payload = {}
    for (const f of props.fields) {
      let value = form[f.key]
      if (f.type === 'number') value = value === '' ? null : Number(value)
      if (f.type === 'select' && value === '') value = null
      payload[f.key] = value
    }
    await props.createFn(payload)
    resetForm()
    await loadRows()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save.'
  } finally {
    submitting.value = false
  }
}

async function handleDelete(id) {
  await props.removeFn(id)
  await loadRows()
}

onMounted(async () => {
  resetForm()
  await Promise.all([loadRows(), loadOptions()])
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
  margin-bottom: 1.5rem;
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

.empty {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.btn-delete {
  background: none;
  border: none;
  color: var(--color-danger);
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0;
}

.add-form {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: flex-end;
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

.field input[type='checkbox'] {
  width: 1.1rem;
  height: 1.1rem;
  align-self: center;
}

button[type='submit'] {
  padding: 0.55rem 1.2rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  height: fit-content;
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
  width: 100%;
}
</style>
