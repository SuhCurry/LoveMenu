<template>
  <div class="min-h-screen bg-gray-50">
    <van-nav-bar
      title="Order Status"
      left-arrow
      @click-left="$router.push('/')"
      fixed
      placeholder
    />

    <div class="p-4">
      <div v-if="loading" class="flex justify-center items-center h-64">
        <van-loading type="spinner" size="24px">Loading...</van-loading>
      </div>

      <div v-else-if="!activeOrder" class="text-center py-20">
        <van-empty description="No active order" />
        <van-button
          type="primary"
          round
          class="mt-4"
          @click="$router.push('/menu')"
        >
          Start Ordering
        </van-button>
      </div>

      <div v-else class="bg-white rounded-lg p-6">
        <!-- Order Info -->
        <div class="mb-6">
          <h2 class="text-xl font-bold mb-2">Order #{{ activeOrder.id }}</h2>
          <p class="text-gray-600 text-sm">
            Placed at: {{ formatDate(activeOrder.order_time) }}
          </p>
          <p v-if="activeOrder.note" class="text-gray-600 text-sm mt-2">
            Note: {{ activeOrder.note }}
          </p>
        </div>

        <!-- Status Steps -->
        <van-steps
          :active="statusStep"
          direction="vertical"
          active-color="#ee0a24"
        >
          <van-step>Ordered</van-step>
          <van-step>Received</van-step>
          <van-step>Cooking</van-step>
          <van-step>Ready to Eat</van-step>
        </van-steps>

        <!-- Order Items -->
        <div class="mt-6">
          <h3 class="text-lg font-semibold mb-3">Order Items</h3>
          <div class="space-y-2">
            <div
              v-for="item in activeOrder.items"
              :key="item.id"
              class="flex justify-between items-center p-2 bg-gray-50 rounded"
            >
              <span class="text-gray-700">{{ item.dish_name }}</span>
              <span class="text-gray-600">x{{ item.quantity }}</span>
            </div>
          </div>
        </div>

        <!-- Refresh Button -->
        <van-button
          type="primary"
          block
          round
          class="mt-6"
          @click="fetchActiveOrder"
          :loading="loading"
        >
          Refresh Status
        </van-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getActiveOrder } from '../api'
import { showToast } from 'vant'

const loading = ref(false)
const activeOrder = ref(null)
let refreshInterval = null

const statusStep = computed(() => {
  if (!activeOrder.value) return 0
  
  const statusMap = {
    'pending': 0,
    'accepted': 1,
    'cooking': 2,
    'completed': 3
  }
  
  return statusMap[activeOrder.value.status] || 0
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchActiveOrder = async () => {
  loading.value = true
  try {
    activeOrder.value = await getActiveOrder()
  } catch (error) {
    if (error.response?.status === 404) {
      activeOrder.value = null
    } else {
      console.error('Error fetching active order:', error)
      showToast.fail('Failed to load order status')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchActiveOrder()
  // Auto-refresh every 5 seconds
  refreshInterval = setInterval(fetchActiveOrder, 5000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>


