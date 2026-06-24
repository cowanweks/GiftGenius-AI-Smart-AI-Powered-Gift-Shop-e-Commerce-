import api from './api'

export const getWishlist = () => api.get('/wishlist/').then((r) => r.data)
export const addToWishlist = (productId) => api.post('/wishlist/', { product: productId }).then((r) => r.data)
export const removeFromWishlist = (id) => api.delete(`/wishlist/${id}/`)
export const moveToCart = (id) => api.post(`/wishlist/${id}/move-to-cart/`).then((r) => r.data)
