import { api } from './client'

export const categories = {
  list: () => api.get('/categories').then((r) => r.data),
  create: (body) => api.post('/categories', body).then((r) => r.data),
  update: (id, body) => api.put(`/categories/${id}`, body).then((r) => r.data),
  remove: (id) => api.delete(`/categories/${id}`),
}

export const products = {
  list: () => api.get('/products').then((r) => r.data),
  create: (body) => api.post('/products', body).then((r) => r.data),
  update: (id, body) => api.put(`/products/${id}`, body).then((r) => r.data),
  remove: (id) => api.delete(`/products/${id}`),
}
