<!-- frontend/src/components/CategoryFilter.vue -->
<!--
  Компонент фильтрации товаров по категориям.
  Отображает список категорий с возможностью выбора для фильтрации.
-->

<template>
  <div class="rounded-2xl border border-ink-200/70 bg-white p-6 shadow-soft lg:sticky lg:top-24">
    <h2 class="mb-5 text-lg font-bold text-ink-900">{{ t('categories.title') }}</h2>

    <!-- Список категорий -->
    <ul class="space-y-1.5">
      <!-- Все категории -->
      <li>
        <button
          @click="selectCategory(null)"
          :class="[
            'flex w-full items-center justify-between rounded-xl px-4 py-2.5 text-sm transition-all duration-200',
            !productsStore.selectedCategory
              ? 'bg-gradient-to-br from-brand-600 to-brand-700 font-semibold text-white shadow-glow'
              : 'font-medium text-ink-600 hover:bg-ink-100 hover:text-ink-900',
          ]"
        >
          <span>{{ t('categories.all') }}</span>
          <span
            v-if="!productsStore.selectedCategory"
            class="rounded-full bg-white/20 px-2 py-0.5 text-xs"
          >
            {{ totalProductsCount }}
          </span>
        </button>
      </li>

      <!-- Отдельные категории -->
      <li v-for="category in productsStore.categories" :key="category.id">
        <button
          @click="selectCategory(category.id)"
          :class="[
            'flex w-full items-center justify-between rounded-xl px-4 py-2.5 text-sm transition-all duration-200',
            productsStore.selectedCategory === category.id
              ? 'bg-gradient-to-br from-brand-600 to-brand-700 font-semibold text-white shadow-glow'
              : 'font-medium text-ink-600 hover:bg-ink-100 hover:text-ink-900',
          ]"
        >
          <span>{{ categoryName(category) }}</span>
          <span
            v-if="productsStore.selectedCategory === category.id"
            class="rounded-full bg-white/20 px-2 py-0.5 text-xs"
          >
            {{ productsStore.productsCount }}
          </span>
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProductsStore } from '@/stores/products'
import { useCategoryName } from '@/composables/useCategoryName'

const { t } = useI18n()
const categoryName = useCategoryName()
const productsStore = useProductsStore()

/**
 * Общее количество товаров (без фильтра)
 */
const totalProductsCount = computed(() => {
  return productsStore.products.length
})

/**
 * Выбрать категорию для фильтрации
 */
function selectCategory(categoryId) {
  if (categoryId === null) {
    productsStore.clearCategoryFilter()
  } else {
    productsStore.setCategory(categoryId)
  }
}
</script>
