<!-- frontend/src/views/VerifyPage.vue -->
<!--
  Страница подтверждения почты кодом из письма.
  Email передаётся через query-параметр (?email=...).
-->

<template>
  <div class="min-h-screen bg-white flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md">
      <!-- Заголовок -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-extrabold text-black mb-2">{{ t('verify.title') }}</h1>
        <p class="text-gray-500">
          {{ t('verify.subtitle') }}
          <span class="font-semibold text-black">{{ email }}</span>
        </p>
      </div>

      <!-- Форма -->
      <form class="space-y-4 border-2 border-black rounded-lg p-8" @submit.prevent="handleVerify">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('verify.codeLabel') }}</label>
          <input
            v-model="code"
            type="text"
            inputmode="numeric"
            maxlength="6"
            required
            autocomplete="one-time-code"
            class="w-full border-2 border-gray-300 rounded-md px-3 py-2 text-black text-center text-2xl tracking-[0.5em] placeholder-gray-400 focus:border-black focus:outline-none"
            placeholder="------"
          />
        </div>

        <!-- Сообщение об ошибке -->
        <p v-if="error" class="text-sm text-red-600">{{ error }}</p>

        <!-- Сообщение об успешной повторной отправке -->
        <p v-if="resentMessage" class="text-sm text-green-600">{{ resentMessage }}</p>

        <!-- Кнопка подтверждения -->
        <button
          type="submit"
          :disabled="loading || code.length < 6"
          class="w-full bg-black text-white font-semibold py-2.5 rounded-md hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? t('auth.pleaseWait') : t('verify.confirmButton') }}
        </button>
      </form>

      <!-- Альтернатива: получить код в Telegram (если бот настроен) -->
      <div v-if="telegramLink" class="mt-6">
        <div class="flex items-center gap-3 mb-4">
          <span class="flex-grow border-t border-gray-200"></span>
          <span class="text-sm text-gray-400">{{ t('verify.or') }}</span>
          <span class="flex-grow border-t border-gray-200"></span>
        </div>
        <a
          :href="telegramLink"
          target="_blank"
          rel="noopener"
          class="flex items-center justify-center gap-2 w-full border-2 border-black text-black font-semibold py-2.5 rounded-md hover:bg-black hover:text-white transition-colors"
        >
          <svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z" />
          </svg>
          {{ t('verify.telegramButton') }}
        </a>
      </div>

      <!-- Повторная отправка кода -->
      <p class="text-center text-sm text-gray-600 mt-6">
        {{ t('verify.didNotReceive') }}
        <button
          class="text-black font-semibold hover:underline ml-1 disabled:opacity-50"
          :disabled="resending"
          @click="handleResend"
        >
          {{ t('verify.resend') }}
        </button>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAuthErrorMessage } from '@/composables/useAuthErrorMessage'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const resolveAuthError = useAuthErrorMessage()

const email = ref(route.query.email || '')
const telegramLink = ref(route.query.tg || '')
const code = ref('')
const error = ref('')
const resentMessage = ref('')
const loading = ref(false)
const resending = ref(false)

// Без email подтверждать нечего — возвращаем на регистрацию
if (!email.value) {
  router.replace('/register')
}

/**
 * Подтвердить код и войти
 */
async function handleVerify() {
  error.value = ''
  resentMessage.value = ''
  loading.value = true
  try {
    await authStore.verify(email.value, code.value)
    router.push('/')
  } catch (err) {
    error.value = resolveAuthError(err, false)
  } finally {
    loading.value = false
  }
}

/**
 * Запросить новый код
 */
async function handleResend() {
  error.value = ''
  resentMessage.value = ''
  resending.value = true
  try {
    await authStore.resendCode(email.value)
    resentMessage.value = t('verify.resent')
  } catch (err) {
    error.value = resolveAuthError(err, false)
  } finally {
    resending.value = false
  }
}
</script>
