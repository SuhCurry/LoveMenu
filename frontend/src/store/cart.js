/**
 * Pinia Store for Cart Management
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref([]) // Array of { dish, quantity }

  // Getters
  const totalItems = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const totalPrice = computed(() => {
    // Note: We don't have price in the schema, so this is a placeholder
    // You can add price field later if needed
    return items.value.length
  })

  const isEmpty = computed(() => {
    return items.value.length === 0
  })

  // Actions
  function addToCart(dish) {
    const existingItem = items.value.find(item => item.dish.id === dish.id)
    
    if (existingItem) {
      existingItem.quantity += 1
    } else {
      items.value.push({
        dish: { ...dish },
        quantity: 1
      })
    }
  }

  function removeFromCart(dishId) {
    const index = items.value.findIndex(item => item.dish.id === dishId)
    if (index > -1) {
      items.value.splice(index, 1)
    }
  }

  function updateQuantity(dishId, quantity) {
    const item = items.value.find(item => item.dish.id === dishId)
    if (item) {
      if (quantity <= 0) {
        removeFromCart(dishId)
      } else {
        item.quantity = quantity
      }
    }
  }

  function incrementQuantity(dishId) {
    const item = items.value.find(item => item.dish.id === dishId)
    if (item) {
      item.quantity += 1
    }
  }

  function decrementQuantity(dishId) {
    const item = items.value.find(item => item.dish.id === dishId)
    if (item) {
      if (item.quantity > 1) {
        item.quantity -= 1
      } else {
        removeFromCart(dishId)
      }
    }
  }

  function clearCart() {
    items.value = []
  }

  function getCartItemsForOrder() {
    return items.value.map(item => ({
      dish_id: item.dish.id,
      quantity: item.quantity
    }))
  }

  return {
    // State
    items,
    // Getters
    totalItems,
    totalPrice,
    isEmpty,
    // Actions
    addToCart,
    removeFromCart,
    updateQuantity,
    incrementQuantity,
    decrementQuantity,
    clearCart,
    getCartItemsForOrder,
  }
})


