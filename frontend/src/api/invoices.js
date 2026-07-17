import { api } from './client'

export const invoices = {
  list: () => api.get('/invoices').then((r) => r.data),
  get: (id) => api.get(`/invoices/${id}`).then((r) => r.data),
  pay: (id) => api.post(`/invoices/${id}/pay`).then((r) => r.data),
}
