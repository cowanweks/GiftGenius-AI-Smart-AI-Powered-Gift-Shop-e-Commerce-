import api from './api'

export const getReminders = () => api.get('/reminders/').then((r) => r.data)
export const addReminder = (payload) => api.post('/reminders/', payload).then((r) => r.data)
export const updateReminder = (id, payload) => api.patch(`/reminders/${id}/`, payload).then((r) => r.data)
export const deleteReminder = (id) => api.delete(`/reminders/${id}/`)
