<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-100 to-purple-100 flex flex-col items-center justify-center p-6">
    <div class="text-center mb-8">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">
        💕 LoveMenu 💕
      </h1>
      <p class="text-xl text-gray-600 mb-2">
        What do you want to eat today, my love?
      </p>
      <p class="text-lg text-gray-500">
        今天想吃什么呀，宝贝？
      </p>
    </div>

    <div class="w-full max-w-sm space-y-4">
      <van-button
        type="primary"
        size="large"
        block
        round
        @click="goToMenu"
        class="bg-pink-500 hover:bg-pink-600"
      >
        🍽️ Start Ordering
      </van-button>

      <van-button
        type="success"
        size="large"
        block
        round
        @click="randomPick"
        :loading="randomLoading"
        class="bg-purple-500 hover:bg-purple-600"
      >
        🎲 Random Picker
      </van-button>
    </div>

    <!-- Random Pick Result -->
    <van-popup
      v-model:show="showRandomResult"
      round
      position="center"
      :style="{ padding: '30px', width: '80%', maxWidth: '400px' }"
    >
      <div class="text-center">
        <div class="text-6xl mb-4 animate-bounce">
          {{ randomDish?.name ? '🍴' : '' }}
        </div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">
          {{ randomDish?.name || 'No dishes available' }}
        </h2>
        <p v-if="randomDish?.category" class="text-gray-500 mb-4">
          Category: {{ randomDish.category }}
        </p>
        <div v-if="randomDish" class="flex gap-2 justify-center mb-4">
          <van-tag
            v-for="tag in randomDishTags"
            :key="tag"
            type="primary"
            class="mx-1"
          >
            {{ tag }}
          </van-tag>
        </div>
        <div class="flex gap-2">
          <van-button
            type="primary"
            block
            @click="addRandomToCart"
            v-if="randomDish"
          >
            Add to Cart
          </van-button>
          <van-button
            block
            @click="showRandomResult = false"
          >
            Close
          </van-button>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getDishes } from '../api'
import { useCartStore } from '../store/cart'

const router = useRouter()
const cartStore = useCartStore()

const randomLoading = ref(false)
const showRandomResult = ref(false)
const randomDish = ref(null)

const goToMenu = () => {
  router.push('/menu')
}

const randomPick = async () => {
  randomLoading.value = true
  try {
    const dishes = await getDishes(null, true)
    if (dishes && dishes.length > 0) {
      const randomIndex = Math.floor(Math.random() * dishes.length)
      randomDish.value = dishes[randomIndex]
      showRandomResult.value = true
    } else {
      randomDish.value = null
      showRandomResult.value = true
    }
  } catch (error) {
    console.error('Error fetching dishes:', error)
    randomDish.value = null
    showRandomResult.value = true
  } finally {
    randomLoading.value = false
  }
}

const addRandomToCart = () => {
  if (randomDish.value) {
    cartStore.addToCart(randomDish.value)
    showRandomResult.value = false
    router.push('/menu')
  }
}

const randomDishTags = computed(() => {
  if (!randomDish.value?.tags) return []
  return randomDish.value.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
})
</script>

