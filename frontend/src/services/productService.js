import api from './api'

export const getProducts = (params) => api.get('/products/', { params }).then((r) => r.data)
export const getProduct = (slug) => api.get(`/products/${slug}/`).then((r) => r.data)
export const getCategories = () => api.get('/products/categories/').then((r) => r.data)
export const getTrending = () => api.get('/products/trending/').then((r) => r.data)
export const getFeatured = () => api.get('/products/featured/').then((r) => r.data)
export const getSalesStats = () => api.get('/products/stats/').then((r) => r.data)
export const createProduct = (payload) => api.post('/products/', payload).then((r) => r.data)
export const updateProduct = (slug, payload) => api.patch(`/products/${slug}/`, payload).then((r) => r.data)
export const deleteProduct = (slug) => api.delete(`/products/${slug}/`)
