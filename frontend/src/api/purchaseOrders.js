import { api } from './client'

export const purchaseOrders = {
  list: () => api.get('/purchase-orders').then((r) => r.data),
  get: (id) => api.get(`/purchase-orders/${id}`).then((r) => r.data),
  create: (body) => api.post('/purchase-orders', body).then((r) => r.data),
  remove: (id) => api.delete(`/purchase-orders/${id}`),
  addItem: (id, body) => api.post(`/purchase-orders/${id}/items`, body).then((r) => r.data),
  removeItem: (id, itemId) => api.delete(`/purchase-orders/${id}/items/${itemId}`),
  receive: (id, warehouseId) =>
    api.post(`/purchase-orders/${id}/receive`, { warehouse_id: warehouseId }).then((r) => r.data),
}
