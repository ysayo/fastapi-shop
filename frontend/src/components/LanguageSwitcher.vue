<!-- frontend/src/components/LanguageSwitcher.vue -->
<!--
  Переключатель языка интерфейса (Русский / English).
-->

<template>
  <div class="flex items-center gap-0.5 rounded-lg bg-ink-100 p-1">
    <button
      v-for="loc in SUPPORTED_LOCALES"
      :key="loc"
      class="rounded-md px-2.5 py-1 text-xs font-bold transition-all"
      :class="
        locale === loc
          ? 'bg-white text-brand-700 shadow-sm'
          : 'text-ink-500 hover:text-ink-800'
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
