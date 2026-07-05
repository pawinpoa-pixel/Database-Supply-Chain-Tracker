import { api } from './client'

export const suppliers = {
  list: () => api.get('/suppliers').then((r) => r.data),
  create: (body) => api.post('/suppliers', body).then((r) => r.data),
  update: (id, body) => api.put(`/suppliers/${id}`, body).then((r) => r.data),
  remove: (id) => api.delete(`/suppliers/${id}`),
}

export const customers = {
  list: () => api.get('/customers').then((r) => r.data),
  create: (body) => api.post('/customers', body).then((r) => r.data),
  update: (id, body) => api.put(`/customers/${id}`, body).then((r) => r.data),
  remove: (id) => api.delete(`/customers/${id}`),
}

export const carriers = {
  list: () => api.get('/carriers').then((r) => r.data),
  create: (body) => api.post('/carriers', body).then((r) => r.data),
  update: (id, body) => api.put(`/carriers/${id}`, body).then((r) => r.data),
  remove: (id) => api.delete(`/carriers/${id}`),
}
