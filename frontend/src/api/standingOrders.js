import { api } from './client'

export const standingOrders = {
  list: () => api.get('/standing-orders').then((r) => r.data),
  get: (id) => api.get(`/standing-orders/${id}`).then((r) => r.data),
  create: (body) => api.post('/standing-orders', body).then((r) => r.data),
  update: (id, body) => api.put(`/standing-orders/${id}`, body).then((r) => r.data),
  remove: (id) => api.delete(`/standing-orders/${id}`),
  addItem: (id, body) => api.post(`/standing-orders/${id}/items`, body).then((r) => r.data),
  removeItem: (id, itemId) => api.delete(`/standing-orders/${id}/items/${itemId}`),
  releaseOrder: (id) => api.post(`/standing-orders/${id}/release-order`).then((r) => r.data),
  generateInvoice: (id) => api.post(`/standing-orders/${id}/generate-invoice`).then((r) => r.data),
}
