import { api } from './client'

export const orders = {
  list: () => api.get('/orders').then((r) => r.data),
  get: (id) => api.get(`/orders/${id}`).then((r) => r.data),
  create: (body) => api.post('/orders', body).then((r) => r.data),
  remove: (id) => api.delete(`/orders/${id}`),
  addItem: (id, body) => api.post(`/orders/${id}/items`, body).then((r) => r.data),
  removeItem: (id, itemId) => api.delete(`/orders/${id}/items/${itemId}`),
  fulfill: (id, warehouseId) =>
    api.post(`/orders/${id}/fulfill`, { warehouse_id: warehouseId }).then((r) => r.data),
}
