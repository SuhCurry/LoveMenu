<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <van-nav-bar
      title="Menu"
      left-arrow
      @click-left="$router.push('/')"
      fixed
      placeholder
    />

    <div class="flex h-[calc(100vh-46px)]">
      <!-- Sidebar - Categories -->
      <van-sidebar v-model="activeCategory" class="w-24 bg-white">
        <van-sidebar-item
          v-for="category in categories"
          :key="category"
          :title="category"
          @click="selectCategory(category)"
        />
      </van-sidebar>

      <!-- Content - Dishes -->
      <div class="flex-1 overflow-y-auto p-4">
        <div v-if="loading" class="flex justify-center items-center h-64">
          <van-loading type="spinner" size="24px">Loading...</van-loading>
        </div>

        <div v-else-if="filteredDishes.length === 0" class="text-center py-20">
          <p class="text-gray-500">No dishes available in this category</p>
        </div>

        <div v-else class="grid grid-cols-1 gap-4">
          <van-card
            v-for="dish in filteredDishes"
            :key="dish.id"
            :title="dish.name"
            :thumb="dish.image_url || 'https://via.placeholder.com/150'"
            class="mb-2"
          >
            <template #tags>
              <div class="flex flex-wrap gap-1 mt-2">
                <van-tag
                  v-for="tag in getDishTags(dish)"
                  :key="tag"
                  type="primary"
                  size="medium"
                >
                  {{ tag }}
                </van-tag>
              </div>
            </template>

            <template #footer>
              <div class="flex items-center justify-between mt-2">
                <div class="flex items-center gap-1">
                  <span class="text-yellow-500">⭐</span>
                  <span class="text-sm text-gray-600">{{ dish.rating }}/5</span>
                </div>
                <van-button
                  type="primary"
                  size="small"
                  round
                  @click="addToCart(dish)"
                >
                  + Add
                </van-button>
              </div>
            </template>
          </van-card>
        </div>
      </div>
    </div>

    <!-- Floating Cart Bar -->
    <div
      v-if="!cartStore.isEmpty"
      class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 shadow-lg z-50"
    >
      <div class="flex items-center justify-between max-w-md mx-auto">
        <div class="flex items-center gap-2">
          <van-badge :content="cartStore.totalItems" max="99">
            <van-icon name="shopping-cart-o" size="24px" />
          </van-badge>
          <span class="text-gray-700 font-medium">
            {{ cartStore.totalItems }} item(s)
          </span>
        </div>
        <van-button
          type="primary"
          size="normal"
          round
          @click="$router.push('/cart')"
        >
          Go to Cart
        </van-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getDishes } from '../api'
import { useCartStore } from '../store/cart'
import { showToast } from 'vant'

const cartStore = useCartStore()
const loading = ref(false)
const dishes = ref([])
const activeCategory = ref(0)

const categories = computed(() => {
  const cats = [...new Set(dishes.value.map(d => d.category))]
  return cats.sort()
})

const filteredDishes = computed(() => {
  if (categories.value.length === 0) return []
  const selectedCategory = categories.value[activeCategory.value]
  return dishes.value.filter(d => d.category === selectedCategory && d.is_available)
})

const selectCategory = (category) => {
  const index = categories.value.indexOf(category)
  if (index > -1) {
    activeCategory.value = index
  }
}

const getDishTags = (dish) => {
  if (!dish.tags) return []
  return dish.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
}

const addToCart = (dish) => {
  cartStore.addToCart(dish)
  showToast.success(`Added ${dish.name} to cart`)
}

const fetchDishes = async () => {
  loading.value = true
  try {
    dishes.value = await getDishes(null, true)
  } catch (error) {
    console.error('Error fetching dishes:', error)
    showToast.fail('Failed to load dishes')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDishes()
})
</script>


