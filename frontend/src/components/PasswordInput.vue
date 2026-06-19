<!-- frontend/src/components/PasswordInput.vue -->
<!--
  Поле ввода пароля с кнопкой-глазом для показа/скрытия введённого текста.
-->

<template>
  <div>
    <label class="mb-1.5 block text-sm font-medium text-ink-700">{{ label }}</label>
    <div class="relative">
      <input
        :value="modelValue"
        :type="visible ? 'text' : 'password'"
        :autocomplete="autocomplete"
        required
        class="w-full rounded-xl border border-ink-200 bg-ink-50 px-3.5 py-2.5 pr-11 text-ink-900 placeholder-ink-400 transition-all focus:border-brand-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-brand-100"
        placeholder="••••••••"
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <!-- Кнопка показать/скрыть пароль -->
      <button
        type="button"
        class="absolute inset-y-0 right-0 flex items-center px-3 text-ink-400 transition-colors hover:text-brand-600"
        :aria-label="visible ? t('auth.hidePassword') : t('auth.showPassword')"
        @click="visible = !visible"
      >
        <!-- Иконка: глаз открыт -->
        <svg
          v-if="!visible"
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
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
          />
        </svg>
        <!-- Иконка: глаз перечёркнут -->
        <svg
          v-else
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
            d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    required: true,
  },
  autocomplete: {
    type: String,
    default: 'current-password',
  },
})

defineEmits(['update:modelValue'])

const visible = ref(false)
</script>
