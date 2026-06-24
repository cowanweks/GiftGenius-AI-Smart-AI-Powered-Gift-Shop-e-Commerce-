import api from './api'

export const register = (payload) => api.post('/users/register/', payload).then((r) => r.data)
export const login = (payload) => api.post('/users/login/', payload).then((r) => r.data)
export const logout = () => api.post('/users/logout/').catch(() => {})
export const getProfile = () => api.get('/users/profile/').then((r) => r.data)
export const updateProfile = (payload) => api.patch('/users/profile/', payload).then((r) => r.data)
export const changePassword = (payload) => api.post('/users/change-password/', payload).then((r) => r.data)
export const getAllUsers = () => api.get('/users/').then((r) => r.data)
