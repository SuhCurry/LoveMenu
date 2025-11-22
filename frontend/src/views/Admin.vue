<template>
  <div class="min-h-screen bg-gray-50">
    <van-nav-bar
      title="Admin Dashboard"
      left-arrow
      @click-left="$router.push('/')"
      fixed
      placeholder
    />

    <!-- Password Protection -->
    <div v-if="!isAuthenticated" class="p-6">
      <van-cell-group inset>
        <van-field
          v-model="password"
          type="password"
          label="Password"
          placeholder="Enter admin password"
          required
        />
      </van-cell-group>
      <van-button
        type="primary"
        block
        round
        class="mt-4"
        @click="checkPassword"
      >
        Login
      </van-button>
    </div>

    <!-- Admin Content -->
    <div v-else>
      <van-tabs v-model:active="activeTab" sticky>
        <!-- Incoming Orders Tab -->
        <van-tab title="Orders" name="orders">
          <div class="p-4">
            <div v-if="ordersLoading" class="flex justify-center items-center h-64">
              <van-loading type="spinner" size="24px">Loading...</van-loading>
            </div>

            <div v-else-if="orders.length === 0" class="text-center py-20">
              <van-empty description="No orders" />
            </div>

            <div v-else class="space-y-4">
              <van-card
                v-for="order in orders"
                :key="order.id"
                :title="`Order #${order.id}`"
                class="mb-4"
              >
                <template #desc>
                  <div class="text-sm text-gray-600 space-y-1">
                    <p>Time: {{ formatDate(order.order_time) }}</p>
                    <p>Status: 
                      <van-tag :type="getStatusType(order.status)">
                        {{ order.status }}
                      </van-tag>
                    </p>
                    <p v-if="order.note">Note: {{ order.note }}</p>
                    <p>Total Items: {{ order.total_items }}</p>
                  </div>
                </template>

                <template #footer>
                  <div class="mt-4">
                    <h4 class="font-semibold mb-2">Items:</h4>
                    <div class="space-y-1">
                      <div
                        v-for="item in order.items"
                        :key="item.id"
                        class="text-sm text-gray-600"
                      >
                        {{ item.dish_name }} x{{ item.quantity }}
                      </div>
                    </div>
                  </div>
                  
                  <div class="flex gap-2 mt-4">
                    <van-button
                      v-if="order.status === 'pending'"
                      type="primary"
                      size="small"
                      @click="updateStatus(order.id, 'accepted')"
                    >
                      Accept
                    </van-button>
                    <van-button
                      v-if="order.status === 'accepted'"
                      type="warning"
                      size="small"
                      @click="updateStatus(order.id, 'cooking')"
                    >
                      Start Cooking
                    </van-button>
                    <van-button
                      v-if="order.status === 'cooking'"
                      type="success"
                      size="small"
                      @click="updateStatus(order.id, 'completed')"
                    >
                      Done
                    </van-button>
                  </div>
                </template>
              </van-card>
            </div>
          </div>
        </van-tab>

        <!-- Dish Manager Tab -->
        <van-tab title="Dishes" name="dishes">
          <div class="p-4">
            <van-button
              type="primary"
              block
              round
              class="mb-4"
              @click="showAddDish = true"
            >
              Add New Dish
            </van-button>

            <div v-if="dishesLoading" class="flex justify-center items-center h-64">
              <van-loading type="spinner" size="24px">Loading...</van-loading>
            </div>

            <div v-else class="space-y-4">
              <van-card
                v-for="dish in dishes"
                :key="dish.id"
                :title="dish.name"
                :thumb="dish.image_url || 'https://via.placeholder.com/150'"
                class="mb-4"
              >
                <template #desc>
                  <div class="text-sm text-gray-600 space-y-1">
                    <p>Category: {{ dish.category }}</p>
                    <p>Rating: {{ dish.rating }}/5</p>
                    <p>Tags: {{ dish.tags || 'None' }}</p>
                  </div>
                </template>

                <template #footer>
                  <div class="flex gap-2 mt-4">
                    <van-switch
                      v-model="dish.is_available"
                      @change="toggleDishAvailability(dish)"
                    />
                    <span class="text-sm text-gray-600 ml-2">
                      {{ dish.is_available ? 'Available' : 'Unavailable' }}
                    </span>
                  </div>
                </template>
              </van-card>
            </div>
          </div>
        </van-tab>
      </van-tabs>
    </div>

    <!-- Add Dish Dialog -->
    <van-popup
      v-model:show="showAddDish"
      round
      position="center"
      :style="{ padding: '20px', width: '90%', maxWidth: '500px' }"
    >
      <h3 class="text-lg font-bold mb-4">Add New Dish</h3>
      <van-form @submit="addDish">
        <van-cell-group inset>
          <van-field
            v-model="newDish.name"
            name="name"
            label="Name"
            placeholder="Dish name"
            :rules="[{ required: true, message: 'Please enter dish name' }]"
          />
          <van-field
            v-model="newDish.category"
            name="category"
            label="Category"
            placeholder="e.g., Meat, Veggie, Soup"
            :rules="[{ required: true, message: 'Please enter category' }]"
          />
          <van-field
            v-model="newDish.image_url"
            name="image_url"
            label="Image URL"
            placeholder="https://..."
          />
          <van-field
            v-model="newDish.tags"
            name="tags"
            label="Tags"
            placeholder="Spicy,Sweet (comma-separated)"
          />
          <van-field
            v-model="newDish.rating"
            name="rating"
            label="Rating"
            type="number"
            placeholder="1-5"
            :rules="[{ required: true, message: 'Please enter rating (1-5)' }]"
          />
        </van-cell-group>
        <div class="flex gap-2 mt-4">
          <van-button
            block
            @click="showAddDish = false"
          >
            Cancel
          </van-button>
          <van-button
            type="primary"
            block
            native-type="submit"
            :loading="addingDish"
          >
            Add
          </van-button>
        </div>
      </van-form>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDishes, createDish, updateDish, getOrders, updateOrderStatus } from '../api'
import { showToast, showSuccessToast } from 'vant'

const isAuthenticated = ref(false)
const password = ref('')
const ADMIN_PASSWORD = 'admin123' // Simple password for MVP

const activeTab = ref('orders')
const orders = ref([])
const ordersLoading = ref(false)
const dishes = ref([])
const dishesLoading = ref(false)

const showAddDish = ref(false)
const addingDish = ref(false)
const newDish = ref({
  name: '',
  category: '',
  image_url: '',
  tags: '',
  rating: 3,
  is_available: true
})

const checkPassword = () => {
  if (password.value === ADMIN_PASSWORD) {
    isAuthenticated.value = true
    fetchOrders()
    fetchDishes()
  } else {
    showToast.fail('Incorrect password')
  }
}

const fetchOrders = async () => {
  ordersLoading.value = true
  try {
    orders.value = await getOrders(50)
  } catch (error) {
    console.error('Error fetching orders:', error)
    showToast.fail('Failed to load orders')
  } finally {
    ordersLoading.value = false
  }
}

const fetchDishes = async () => {
  dishesLoading.value = true
  try {
    dishes.value = await getDishes(null, false) // Get all dishes including unavailable
  } catch (error) {
    console.error('Error fetching dishes:', error)
    showToast.fail('Failed to load dishes')
  } finally {
    dishesLoading.value = false
  }
}

const updateStatus = async (orderId, status) => {
  try {
    await updateOrderStatus(orderId, status)
    showSuccessToast('Status updated')
    fetchOrders()
  } catch (error) {
    console.error('Error updating status:', error)
    showToast.fail('Failed to update status')
  }
}

const toggleDishAvailability = async (dish) => {
  try {
    await updateDish(dish.id, { is_available: dish.is_available })
    showSuccessToast('Dish updated')
  } catch (error) {
    console.error('Error updating dish:', error)
    showToast.fail('Failed to update dish')
    // Revert the change
    dish.is_available = !dish.is_available
  }
}

const addDish = async () => {
  addingDish.value = true
  try {
    const dishData = {
      ...newDish.value,
      rating: parseInt(newDish.value.rating) || 3
    }
    await createDish(dishData)
    showSuccessToast('Dish added')
    showAddDish.value = false
    // Reset form
    newDish.value = {
      name: '',
      category: '',
      image_url: '',
      tags: '',
      rating: 3,
      is_available: true
    }
    fetchDishes()
  } catch (error) {
    console.error('Error adding dish:', error)
    showToast.fail('Failed to add dish')
  } finally {
    addingDish.value = false
  }
}

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

const getStatusType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'accepted': 'primary',
    'cooking': 'warning',
    'completed': 'success'
  }
  return typeMap[status] || 'default'
}
</script>


