import api from './api'

export const getGiftRecommendations = (payload) =>
  api.post('/recommendations/gift-finder/', payload).then((r) => r.data)
