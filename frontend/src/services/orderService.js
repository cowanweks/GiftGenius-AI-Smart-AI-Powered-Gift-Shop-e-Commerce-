import api from './api'

export const checkout = (payload) => api.post('/orders/checkout/', payload).then((r) => r.data)
export const getOrders = (all = false) =>
  api.get('/orders/', { params: all ? { all: 'true' } : {} }).then((r) => r.data)
export const getOrder = (id) => api.get(`/orders/${id}/`).then((r) => r.data)
export const updateOrderStatus = (id, status) =>
  api.patch(`/orders/${id}/status/`, { status }).then((r) => r.data)
