/**
 * API Service - Axios instance and API functions
 */
import axios from 'axios'

// Create Axios instance
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Dishes API
export const getDishes = async (category = null, availableOnly = true) => {
  const params = {}
  if (category) params.category = category
  if (availableOnly !== null) params.available_only = availableOnly
  
  const response = await api.get('/dishes', { params })
  return response.data
}

export const getDish = async (dishId) => {
  const response = await api.get(`/dishes/${dishId}`)
  return response.data
}

export const createDish = async (dishData) => {
  const response = await api.post('/dishes', dishData)
  return response.data
}

export const updateDish = async (dishId, dishData) => {
  const response = await api.put(`/dishes/${dishId}`, dishData)
  return response.data
}

// Orders API
export const createOrder = async (orderData) => {
  const response = await api.post('/orders', orderData)
  return response.data
}

export const getOrders = async (limit = 20) => {
  const response = await api.get('/orders', { params: { limit } })
  return response.data
}

export const getActiveOrder = async () => {
  const response = await api.get('/orders/active')
  return response.data
}

export const getOrder = async (orderId) => {
  const response = await api.get(`/orders/${orderId}`)
  return response.data
}

export const updateOrderStatus = async (orderId, status) => {
  const response = await api.patch(`/orders/${orderId}/status`, { status })
  return response.data
}

export default api


