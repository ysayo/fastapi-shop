<!-- frontend/src/views/HomePage.vue -->
<!--
  Главная страница с каталогом товаров.
  Отображает список товаров и фильтр по категориям.
-->

<template>
  <div class="min-h-screen">
    <!-- Геро-баннер -->
    <section class="relative overflow-hidden border-b border-ink-200/70 bg-ink-950">
      <div
        class="absolute inset-0 bg-gradient-to-br from-brand-700 via-brand-600 to-brand-900 opacity-90"
      ></div>
      <div
        class="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-brand-400/30 blur-3xl"
      ></div>
      <div
        class="pointer-events-none absolute -left-16 bottom-0 h-64 w-64 rounded-full bg-fuchsia-500/20 blur-3xl"
      ></div>
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-20">
        <span
          class="inline-flex items-center rounded-full bg-white/15 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-white/90 backdrop-blur"
        >
          FastAPI Shop
        </span>
        <h1 class="mt-5 max-w-2xl text-4xl font-extrabold tracking-tight text-white sm:text-5xl">
          {{ t('home.title') }}
        </h1>
        <p class="mt-4 max-w-xl text-lg text-white/80">{{ t('home.subtitle') }}</p>
      </div>
    </section>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Боковая панель с фильтром -->
        <aside class="w-full lg:w-64 lg:flex-shrink-0">
          <CategoryFilter />
        </aside>

        <!-- Основное содержимое -->
        <main class="flex-grow">
          <!-- Информация о фильтрации -->
          <div class="mb-6 flex items-center justify-between">
            <p class="text-sm font-medium text-ink-500">
              {{ t('home.productsFound', productsStore.productsCount) }}
            </p>

            <!-- Кнопка сброса фильтра -->
            <button
              v-if="productsStore.selectedCategory"
              @click="productsStore.clearCategoryFilter"
              class="inline-flex items-center gap-1 rounded-lg px-3 py-1.5 text-sm font-medium text-brand-700 hover:bg-brand-50 transition-colors"
            >
              {{ t('home.clearFilter') }}
            </button>
          </div>

          <!-- Состояние загрузки -->
          <div v-if="productsStore.loading" class="flex flex-col items-center py-20">
            <div
              class="h-12 w-12 animate-spin rounded-full border-4 border-ink-200 border-t-brand-600"
            ></div>
            <p class="mt-4 text-ink-500">{{ t('home.loading') }}</p>
          </div>

          <!-- Ошибка -->
          <div
            v-else-if="productsStore.error"
            class="rounded-2xl border border-red-100 bg-red-50 py-12 text-center"
          >
            <p class="font-medium text-red-600">{{ t(productsStore.error) }}</p>
          </div>

          <!-- Список товаров -->
          <div
            v-else-if="productsStore.filteredProducts.length > 0"
            class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            <ProductCard
              v-for="product in productsStore.filteredProducts"
              :key="product.id"
              :product="product"
            />
          </div>

          <!-- Пустое состояние -->
          <div
            v-else
            class="flex flex-col items-center rounded-2xl border border-dashed border-ink-200 bg-white py-16 text-center"
          >
            <div class="flex h-16 w-16 items-center justify-center rounded-2xl bg-ink-100">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8 text-ink-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
                />
              </svg>
            </div>
            <p class="mt-4 text-lg font-semibold text-ink-700">{{ t('home.noProducts') }}</p>
            <button
              @click="productsStore.clearCategoryFilter"
              class="mt-4 rounded-lg bg-brand-50 px-4 py-2 text-sm font-semibold text-brand-700 hover:bg-brand-100 transition-colors"
            >
              {{ t('home.viewAll') }}
            </button>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProductsStore } from '@/stores/products'
import ProductCard from '@/components/ProductCard.vue'
import CategoryFilter from '@/components/CategoryFilter.vue'

const { t } = useI18n()
const productsStore = useProductsStore()

/**
 * Загрузить данные при монтировании компонента
 */
onMounted(async () => {
  await Promise.all([productsStore.fetchProducts(), productsStore.fetchCategories()])
})
</script>
