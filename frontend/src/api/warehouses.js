import { api } from './client'

export const warehouses = {
  list: () => api.get('/warehouses').then((r) => r.data),
  create: (body) => api.post('/warehouses', body).then((r) => r.data),
  update: (id, body) => api.put(`/warehouses/${id}`, body).then((r) => r.data),
  remove: (id) => api.delete(`/warehouses/${id}`),
}

export const inventory = {
  list: () => api.get('/inventory').then((r) => r.data),
  lowStock: () => api.get('/inventory/low-stock').then((r) => r.data),
  create: (body) => api.post('/inventory', body).then((r) => r.data),
  update: (id, body) => api.put(`/inventory/${id}`, body).then((r) => r.data),
  remove: (id) => api.delete(`/inventory/${id}`),
}

export const inventoryLogs = {
  list: (params) => api.get('/inventory-logs', { params }).then((r) => r.data),
}
