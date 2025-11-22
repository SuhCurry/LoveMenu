<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <van-nav-bar
      title="Shopping Cart"
      left-arrow
      @click-left="$router.push('/menu')"
      fixed
      placeholder
    />

    <div v-if="cartStore.isEmpty" class="flex flex-col items-center justify-center h-64">
      <van-empty description="Your cart is empty" />
      <van-button
        type="primary"
        round
        class="mt-4"
        @click="$router.push('/menu')"
      >
        Go to Menu
      </van-button>
    </div>

    <div v-else class="p-4 space-y-4">
      <!-- Cart Items -->
      <van-card
        v-for="item in cartStore.items"
        :key="item.dish.id"
        :title="item.dish.name"
        :thumb="item.dish.image_url || 'https://via.placeholder.com/150'"
        class="mb-4"
      >
        <template #tags>
          <div class="flex flex-wrap gap-1 mt-2">
            <van-tag
              v-for="tag in getDishTags(item.dish)"
              :key="tag"
              type="primary"
              size="small"
            >
              {{ tag }}
            </van-tag>
          </div>
        </template>

        <template #footer>
          <div class="flex items-center justify-between mt-4">
            <div class="flex items-center gap-3">
              <van-button
                size="small"
                round
                @click="cartStore.decrementQuantity(item.dish.id)"
              >
                -
              </van-button>
              <span class="text-lg font-semibold w-8 text-center">
                {{ item.quantity }}
              </span>
              <van-button
                type="primary"
                size="small"
                round
                @click="cartStore.incrementQuantity(item.dish.id)"
              >
                +
              </van-button>
            </div>
            <van-button
              type="danger"
              size="small"
              round
              @click="cartStore.removeFromCart(item.dish.id)"
            >
              Remove
            </van-button>
          </div>
        </template>
      </van-card>

      <!-- Special Request -->
      <div class="bg-white rounded-lg p-4 mt-4">
        <h3 class="text-lg font-semibold mb-2">Special Request</h3>
        <van-field
          v-model="note"
          type="textarea"
          placeholder="e.g., Less salt, No spicy..."
          rows="3"
          maxlength="200"
          show-word-limit
        />
      </div>

      <!-- Summary -->
      <div class="bg-white rounded-lg p-4">
        <div class="flex justify-between items-center mb-2">
          <span class="text-gray-600">Total Items:</span>
          <span class="font-semibold">{{ cartStore.totalItems }}</span>
        </div>
      </div>

      <!-- Submit Button -->
      <van-button
        type="primary"
        size="large"
        block
        round
        :loading="submitting"
        @click="placeOrder"
        class="mt-6"
      >
        Place Order
      </van-button>
    </div>

    <!-- Success Popup -->
    <van-popup
      v-model:show="showSuccess"
      round
      position="center"
      :style="{ padding: '30px', width: '80%', maxWidth: '400px' }"
    >
      <div class="text-center">
        <div class="text-6xl mb-4">🎉</div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">Order Placed!</h2>
        <p class="text-gray-600 mb-4">Your order has been submitted successfully</p>
        <van-button
          type="primary"
          block
          @click="goToStatus"
        >
          View Status
        </van-button>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../store/cart'
import { createOrder } from '../api'
import { showToast, showSuccessToast } from 'vant'

const router = useRouter()
const cartStore = useCartStore()

const note = ref('')
const submitting = ref(false)
const showSuccess = ref(false)

const getDishTags = (dish) => {
  if (!dish.tags) return []
  return dish.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
}

const placeOrder = async () => {
  if (cartStore.isEmpty) {
    showToast.fail('Cart is empty')
    return
  }

  submitting.value = true
  try {
    const orderData = {
      items: cartStore.getCartItemsForOrder(),
      note: note.value || null
    }

    await createOrder(orderData)
    cartStore.clearCart()
    showSuccess.value = true
  } catch (error) {
    console.error('Error placing order:', error)
    showToast.fail('Failed to place order. Please try again.')
  } finally {
    submitting.value = false
  }
}

const goToStatus = () => {
  showSuccess.value = false
  router.push('/status')
}
</script>


