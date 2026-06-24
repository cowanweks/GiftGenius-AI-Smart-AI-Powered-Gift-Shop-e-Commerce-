import api from './api'

export const getCart = () => api.get('/cart/').then((r) => r.data)
export const addToCart = (productId, quantity = 1) =>
  api.post('/cart/', { product: productId, quantity }).then((r) => r.data)
export const updateCartItem = (id, quantity) => api.patch(`/cart/${id}/`, { quantity }).then((r) => r.data)
export const removeCartItem = (id) => api.delete(`/cart/${id}/`)
export const clearCart = () => api.delete('/cart/clear/')
