import { api } from './client'

export const shipments = {
  list: () => api.get('/shipments').then((r) => r.data),
  get: (id) => api.get(`/shipments/${id}`).then((r) => r.data),
  create: (body) => api.post('/shipments', body).then((r) => r.data),
  remove: (id) => api.delete(`/shipments/${id}`),
  addItem: (id, body) => api.post(`/shipments/${id}/items`, body).then((r) => r.data),
  removeItem: (id, itemId) => api.delete(`/shipments/${id}/items/${itemId}`),
  ship: (id) => api.post(`/shipments/${id}/ship`).then((r) => r.data),
  deliver: (id) => api.post(`/shipments/${id}/deliver`).then((r) => r.data),
  history: (id) => api.get(`/shipments/${id}/history`).then((r) => r.data),
}
