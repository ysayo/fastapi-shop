<!-- frontend/src/components/LanguageSwitcher.vue -->
<!--
  Переключатель языка интерфейса (Русский / English).
-->

<template>
  <div class="flex items-center border-2 border-black rounded-md overflow-hidden">
    <button
      v-for="loc in SUPPORTED_LOCALES"
      :key="loc"
      class="px-3 py-1.5 text-sm font-semibold transition-colors"
      :class="
        locale === loc ? 'bg-black text-white' : 'bg-white text-black hover:bg-gray-100'
      "
      @click="setLocale(loc)"
    >
      {{ loc.toUpperCase() }}
    </button>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { setLocale, SUPPORTED_LOCALES } from '@/i18n'

const { locale } = useI18n()
</script>
