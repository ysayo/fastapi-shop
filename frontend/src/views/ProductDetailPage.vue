<!-- frontend/src/views/ProductDetailPage.vue -->
<!--
  Детальная страница товара.
  Отображает полную информацию о товаре с возможностью добавления в корзину.
-->

<template>
  <div class="min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <!-- Кнопка "Назад" -->
      <button
        @click="router.push('/')"
        class="group mb-8 inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-ink-500 transition-colors hover:bg-ink-100 hover:text-ink-900 dark:text-ink-400 dark:hover:bg-ink-800 dark:hover:text-ink-50"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 transition-transform group-hover:-translate-x-0.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 19l-7-7 7-7"
          />
        </svg>
        {{ t('product.backToCatalog') }}
      </button>

      <!-- Состояние загрузки -->
      <div v-if="loading" class="flex flex-col items-center py-20">
        <div class="h-14 w-14 animate-spin rounded-full border-4 border-ink-200 border-t-brand-600 dark:border-ink-700 dark:border-t-brand-500"></div>
        <p class="mt-4 text-lg text-ink-500 dark:text-ink-400">{{ t('product.loading') }}</p>
      </div>

      <!-- Ошибка -->
      <div
        v-else-if="error"
        class="rounded-2xl border border-red-100 bg-red-50 py-16 text-center dark:border-red-500/20 dark:bg-red-500/10"
      >
        <p class="text-lg font-medium text-red-600 dark:text-red-400">{{ error }}</p>
        <button
          @click="router.push('/')"
          class="mt-6 inline-flex items-center rounded-xl bg-gradient-to-br from-brand-600 to-brand-700 py-3 px-8 text-base font-semibold text-white shadow-glow transition-all hover:from-brand-500 hover:to-brand-600"
        >
          {{ t('product.returnToCatalog') }}
        </button>
      </div>

      <!-- Детальная информация о товаре -->
      <div
        v-else-if="product"
        class="overflow-hidden rounded-3xl border border-ink-200/70 bg-white shadow-soft dark:border-ink-800 dark:bg-ink-900"
      >
        <div class="grid grid-cols-1 md:grid-cols-2">
          <!-- Изображение -->
          <div class="flex aspect-square items-center justify-center overflow-hidden bg-white p-8 md:p-10">
            <img
              :src="product.image_url"
              :alt="product.name"
              class="max-h-full max-w-full object-contain"
              @error="handleImageError"
            />
          </div>

          <!-- Информация -->
          <div class="flex flex-col p-8 sm:p-10">
            <!-- Категория -->
            <div>
              <span
                class="inline-flex items-center rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-brand-700 dark:bg-brand-500/10 dark:text-brand-300"
              >
                {{ categoryName(product.category) }}
              </span>
            </div>

            <!-- Название -->
            <h1 class="mt-4 text-3xl sm:text-4xl font-extrabold tracking-tight text-ink-900 dark:text-ink-50">
              {{ localized(product, 'name') }}
            </h1>

            <!-- Цена -->
            <div class="mt-4 text-3xl font-extrabold tracking-tight text-ink-900 dark:text-ink-50">
              ${{ product.price.toFixed(2) }}
            </div>

            <!-- Описание -->
            <div class="mt-8">
              <h2 class="mb-2 text-sm font-bold uppercase tracking-wide text-ink-400 dark:text-ink-500">
                {{ t('product.description') }}
              </h2>
              <p class="leading-relaxed text-ink-600 dark:text-ink-300">
                {{ localized(product, 'description') || t('product.noDescription') }}
              </p>
            </div>

            <!-- Кнопка добавления в корзину -->
            <div class="mt-8">
              <button
                @click="handleAddToCart"
                :disabled="adding"
                class="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-br from-brand-600 to-brand-700 py-4 px-6 text-base font-semibold text-white shadow-glow transition-all hover:from-brand-500 hover:to-brand-600 active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-50"
              >
                <svg
                  v-if="!adding"
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
                {{ adding ? t('product.addingToCart') : t('product.addToCart') }}
              </button>

              <!-- Уведомление об успешном добавлении -->
              <transition name="fade">
                <div
                  v-if="showNotification"
                  class="mt-4 flex items-center justify-center gap-2 rounded-xl bg-emerald-50 px-4 py-3 text-center font-medium text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400"
                >
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  {{ t('product.addedNotification') }}
                </div>
              </transition>
            </div>

            <!-- Дополнительная информация -->
            <div class="mt-8 space-y-1 border-t border-ink-200 pt-6 dark:border-ink-800">
              <p class="text-sm text-ink-400 dark:text-ink-500">{{ t('product.id', { id: product.id }) }}</p>
              <p class="text-sm text-ink-400 dark:text-ink-500">{{ t('product.added', { date: formatDate(product.created_at) }) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/products'
import { useCartStore } from '@/stores/cart'
import { useCategoryName } from '@/composables/useCategoryName'
import { useLocalized } from '@/composables/useLocalized'

const { t, locale } = useI18n()
const categoryName = useCategoryName()
const localized = useLocalized()
const route = useRoute()
const router = useRouter()
const productsStore = useProductsStore()
const cartStore = useCartStore()

// State
const product = ref(null)
const loading = ref(false)
const error = ref(null)
const adding = ref(false)
const showNotification = ref(false)

/**
 * Загрузить данные товара
 */
async function loadProduct() {
  loading.value = true
  error.value = null

  try {
    const productId = parseInt(route.params.id)
    product.value = await productsStore.fetchProductById(productId)
  } catch (err) {
    error.value = t('product.notFound')
    console.error('Error loading product:', err)
  } finally {
    loading.value = false
  }
}

/**
 * Добавить товар в корзину
 */
async function handleAddToCart() {
  adding.value = true
  const success = await cartStore.addToCart(product.value.id, 1)

  if (success) {
    showNotification.value = true
    setTimeout(() => {
      showNotification.value = false
    }, 3000)
  }

  adding.value = false
}

/**
 * Форматировать дату
 */
function formatDate(dateString) {
  const date = new Date(dateString)
  const localeTag = locale.value === 'ru' ? 'ru-RU' : 'en-US'
  return date.toLocaleDateString(localeTag, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

/**
 * Обработка ошибки загрузки изображения
 */
function handleImageError(event) {
  event.target.src = 'https://via.placeholder.com/600x600?text=No+Image'
}

// Загрузить товар при монтировании
onMounted(() => {
  loadProduct()
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
