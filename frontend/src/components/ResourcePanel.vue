<template>
  <div class="master-panel">
    <div class="panel-titlebar">
      <span class="titlebar-mark" />
      <h2>{{ title }}</h2>
      <span v-if="editingId" class="editing-badge">Editing record #{{ editingId }}</span>
    </div>

    <form class="detail-form" @submit.prevent="handleSubmit">
      <div class="form-grid">
        <div class="form-field" v-for="f in fields" :key="f.key" :class="{ 'is-checkbox': f.type === 'checkbox' }">
          <template v-if="f.type === 'checkbox'">
            <label class="checkbox-field">
              <input type="checkbox" v-model="form[f.key]" />
              <span>{{ f.label }}</span>
            </label>
          </template>
          <template v-else>
            <label>{{ f.label }}<span v-if="f.required" class="required">*</span></label>
            <select v-if="f.type === 'select'" v-model="form[f.key]" :required="f.required">
              <option value="" disabled>Select...</option>
              <option v-for="opt in optionsCache[f.key] || []" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </option>
            </select>
            <input
              v-else
              :type="f.type"
              :step="f.step"
              v-model="form[f.key]"
              :required="f.required"
            />
          </template>
        </div>
      </div>

      <p v-if="error" class="form-error">{{ error }}</p>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="submitting">
          <IconSave />
          {{ submitting ? 'Saving...' : editingId ? 'Update' : 'Save' }}
        </button>
        <button type="button" class="btn btn-outline" @click="handleExport">
          <IconExport />
          Export
        </button>
        <button type="button" class="btn btn-ghost" @click="handleReset">
          <IconReset />
          Reset
        </button>
      </div>
    </form>

    <div class="table-toolbar">
      <div class="record-count">Total Record(s) Found: <strong>{{ filteredRows.length }}</strong></div>
      <div class="search-box">
        <IconSearch />
        <input v-model="search" type="text" placeholder="Search..." />
      </div>
    </div>

    <div class="table-scroll">
      <table v-if="pagedRows.length" class="data-grid">
        <thead>
          <tr>
            <th class="col-icon">Edit</th>
            <th class="col-icon">Del</th>
            <th v-for="f in fields" :key="f.key">{{ f.label }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in pagedRows" :key="row.id" :class="{ 'is-editing': row.id === editingId }">
            <td class="col-icon">
              <button class="icon-btn icon-edit" title="Edit" @click="startEdit(row)">
                <IconPencil />
              </button>
            </td>
            <td class="col-icon">
              <button class="icon-btn icon-delete" title="Delete" @click="handleDelete(row.id)">
                <IconTrash />
              </button>
            </td>
            <td v-for="f in fields" :key="f.key">{{ displayValue(row, f) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No records found.</p>
    </div>

    <div class="table-footer" v-if="filteredRows.length">
      <span class="footer-count">
        Records {{ startIndex + 1 }}-{{ endIndex }} of {{ filteredRows.length }}
      </span>
      <div class="pagination">
        <button class="page-btn" :disabled="page === 1" @click="page = 1">First</button>
        <button class="page-btn" :disabled="page === 1" @click="page--">Prev</button>
        <button
          v-for="p in totalPages"
          :key="p"
          class="page-btn page-num"
          :class="{ active: p === page }"
          @click="page = p"
        >
          {{ p }}
        </button>
        <button class="page-btn" :disabled="page === totalPages" @click="page++">Next</button>
        <button class="page-btn" :disabled="page === totalPages" @click="page = totalPages">Last</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import IconPencil from './icons/IconPencil.vue'
import IconTrash from './icons/IconTrash.vue'
import IconSearch from './icons/IconSearch.vue'
import IconSave from './icons/IconSave.vue'
import IconExport from './icons/IconExport.vue'
import IconReset from './icons/IconReset.vue'

const props = defineProps({
  title: { type: String, required: true },
  fields: { type: Array, required: true },
  listFn: { type: Function, required: true },
  createFn: { type: Function, required: true },
  removeFn: { type: Function, required: true },
  updateFn: { type: Function, default: null },
})

const PAGE_SIZE = 8

const rows = ref([])
const form = reactive({})
const optionsCache = reactive({})
const error = ref('')
const submitting = ref(false)
const editingId = ref(null)
const search = ref('')
const page = ref(1)

function defaultFor(f) {
  if (f.default !== undefined) return f.default
  return f.type === 'checkbox' ? true : ''
}

function resetForm() {
  editingId.value = null
  for (const f of props.fields) form[f.key] = defaultFor(f)
  error.value = ''
}

function displayValue(row, f) {
  if (f.display) return f.display(row)
  return row[f.key]
}

const filteredRows = computed(() => {
  const term = search.value.trim().toLowerCase()
  if (!term) return rows.value
  return rows.value.filter((row) => {
    if (String(row.id).includes(term)) return true
    return props.fields.some((f) => String(displayValue(row, f) ?? '').toLowerCase().includes(term))
  })
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredRows.value.length / PAGE_SIZE)))
const startIndex = computed(() => (page.value - 1) * PAGE_SIZE)
const endIndex = computed(() => Math.min(startIndex.value + PAGE_SIZE, filteredRows.value.length))
const pagedRows = computed(() => filteredRows.value.slice(startIndex.value, endIndex.value))

watch(search, () => {
  page.value = 1
})

watch(totalPages, (max) => {
  if (page.value > max) page.value = max
})

async function loadRows() {
  rows.value = await props.listFn()
}

async function loadOptions() {
  for (const f of props.fields) {
    if (f.optionsSource) optionsCache[f.key] = await f.optionsSource()
  }
}

function startEdit(row) {
  editingId.value = row.id
  for (const f of props.fields) {
    form[f.key] = row[f.key] ?? defaultFor(f)
  }
  error.value = ''
}

function buildPayload() {
  const payload = {}
  for (const f of props.fields) {
    let value = form[f.key]
    if (f.type === 'number') value = value === '' ? null : Number(value)
    if (f.type === 'select' && value === '') value = null
    payload[f.key] = value
  }
  return payload
}

async function handleSubmit() {
  error.value = ''
  submitting.value = true
  try {
    const payload = buildPayload()
    if (editingId.value && props.updateFn) {
      await props.updateFn(editingId.value, payload)
    } else {
      await props.createFn(payload)
    }
    resetForm()
    await loadRows()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save.'
  } finally {
    submitting.value = false
  }
}

function handleReset() {
  resetForm()
}

async function handleDelete(id) {
  if (!confirm('Delete this record?')) return
  await props.removeFn(id)
  if (editingId.value === id) resetForm()
  await loadRows()
}

function handleExport() {
  const header = ['ID', ...props.fields.map((f) => f.label)]
  const lines = [header]
  for (const row of filteredRows.value) {
    lines.push([row.id, ...props.fields.map((f) => displayValue(row, f) ?? '')])
  }
  const csv = lines
    .map((line) => line.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(','))
    .join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${props.title.toLowerCase().replace(/\s+/g, '-')}.csv`
  link.click()
  URL.revokeObjectURL(url)
}

onMounted(async () => {
  resetForm()
  await Promise.all([loadRows(), loadOptions()])
})
</script>

<style scoped>
.master-panel {
  background: var(--color-surface);
  border-radius: 14px;
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.panel-titlebar {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.9rem 1.5rem;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
}

.titlebar-mark {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  background: var(--color-sidebar-accent);
  flex-shrink: 0;
}

.panel-titlebar h2 {
  font-size: 1.05rem;
  color: white;
  font-weight: 600;
}

.editing-badge {
  margin-left: auto;
  background: rgba(255, 255, 255, 0.18);
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
}

.detail-form {
  padding: 1.5rem 1.5rem 1.25rem;
  border-bottom: 1px solid var(--color-border-subtle);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem 1.25rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-field label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-text-muted);
}

.required {
  color: var(--color-danger);
  margin-left: 0.15rem;
}

.form-field input,
.form-field select {
  padding: 0.55rem 0.7rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 0.9rem;
  background: var(--color-bg-alt);
  color: var(--color-text);
  transition: border-color 0.15s, background 0.15s;
}

.form-field input:focus,
.form-field select:focus {
  outline: none;
  border-color: var(--color-primary);
  background: var(--color-surface);
}

.form-field.is-checkbox {
  justify-content: flex-end;
}

.checkbox-field {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-text);
  cursor: pointer;
}

.checkbox-field input {
  width: 1.05rem;
  height: 1.05rem;
}

.form-error {
  color: var(--color-danger);
  font-size: 0.85rem;
  margin-top: 0.9rem;
}

.form-actions {
  display: flex;
  gap: 0.6rem;
  margin-top: 1.1rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.55rem 1.1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  border: 1px solid transparent;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.btn-outline {
  background: transparent;
  border-color: var(--color-border);
  color: var(--color-text);
}

.btn-outline:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.btn-ghost {
  background: transparent;
  color: var(--color-text-muted);
}

.btn-ghost:hover {
  color: var(--color-danger);
}

.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.record-count {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

.record-count strong {
  color: var(--color-text);
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.45rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-bg-alt);
  min-width: 220px;
}

.search-box svg {
  color: var(--color-text-subtle);
  flex-shrink: 0;
}

.search-box input {
  border: none;
  background: none;
  outline: none;
  font-size: 0.88rem;
  color: var(--color-text);
  width: 100%;
}

.table-scroll {
  overflow-x: auto;
  padding: 0 1.5rem;
}

.data-grid {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
  white-space: nowrap;
}

.data-grid th {
  text-align: left;
  padding: 0.55rem 0.7rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--color-text-muted);
  border-bottom: 2px solid var(--color-border-subtle);
}

.data-grid td {
  padding: 0.55rem 0.7rem;
  border-bottom: 1px solid var(--color-border-subtle);
  color: var(--color-text);
}

.data-grid .col-icon {
  width: 2.2rem;
  text-align: center;
}

.data-grid tbody tr:nth-child(even) {
  background: var(--color-bg-alt);
}

.data-grid tbody tr:hover {
  background: var(--color-primary-tint);
}

.data-grid tbody tr.is-editing {
  background: var(--color-primary-tint);
  box-shadow: inset 3px 0 0 var(--color-primary);
}

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.8rem;
  height: 1.8rem;
  border: none;
  border-radius: 6px;
  background: none;
  cursor: pointer;
}

.icon-edit {
  color: var(--color-primary);
}

.icon-edit:hover {
  background: var(--color-primary-tint);
}

.icon-delete {
  color: var(--color-danger);
}

.icon-delete:hover {
  background: var(--color-danger-tint);
}

.empty {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  padding: 1.5rem 0;
  text-align: center;
}

.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding: 1rem 1.5rem 1.5rem;
}

.footer-count {
  font-size: 0.82rem;
  color: var(--color-text-muted);
}

.pagination {
  display: flex;
  gap: 0.3rem;
  flex-wrap: wrap;
}

.page-btn {
  padding: 0.35rem 0.65rem;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text);
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
}

.page-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.page-btn:hover:not(:disabled):not(.active) {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.page-btn.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}
</style>
