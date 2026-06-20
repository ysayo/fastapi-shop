<!-- frontend/src/views/VerifyPage.vue -->
<!--
  Страница подтверждения почты кодом из письма.
  Email передаётся через query-параметр (?email=...).
-->

<template>
  <div class="relative flex min-h-[calc(100vh-5rem)] items-center justify-center overflow-hidden px-4 py-12">
    <!-- Декоративный фон -->
    <div
      class="pointer-events-none absolute -top-24 left-1/2 h-72 w-72 -translate-x-1/2 rounded-full bg-brand-200/40 blur-3xl"
    ></div>

    <div class="relative w-full max-w-md">
      <!-- Заголовок -->
      <div class="mb-8 text-center">
        <div
          class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 text-white shadow-glow"
        >
          <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
        </div>
        <h1 class="text-2xl font-extrabold tracking-tight text-ink-900 dark:text-ink-50 mb-1">{{ t('verify.title') }}</h1>
        <p class="text-ink-500 dark:text-ink-400">
          {{ t('verify.subtitle') }}
          <span class="font-semibold text-ink-900 dark:text-ink-100">{{ email }}</span>
        </p>
      </div>

      <!-- Форма -->
      <form
        class="space-y-4 rounded-2xl border border-ink-200/70 bg-white p-8 shadow-card dark:border-ink-800 dark:bg-ink-900"
        @submit.prevent="handleVerify"
      >
        <div>
          <label class="mb-1.5 block text-sm font-medium text-ink-700 dark:text-ink-200">{{ t('verify.codeLabel') }}</label>
          <input
            v-model="code"
            type="text"
            inputmode="numeric"
            maxlength="6"
            required
            autocomplete="one-time-code"
            class="w-full rounded-xl border border-ink-200 bg-ink-50 px-3.5 py-3 text-center text-2xl font-semibold tracking-[0.5em] text-ink-900 placeholder-ink-300 transition-all focus:border-brand-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-800 dark:text-ink-50 dark:placeholder-ink-600 dark:focus:bg-ink-800 dark:focus:ring-brand-500/20"
            placeholder="------"
          />
        </div>

        <!-- Сообщение об ошибке -->
        <p
          v-if="error"
          class="rounded-xl bg-red-50 px-3.5 py-2.5 text-sm font-medium text-red-600 dark:bg-red-500/10 dark:text-red-400"
        >
          {{ error }}
        </p>

        <!-- Сообщение об успешной повторной отправке -->
        <p
          v-if="resentMessage"
          class="rounded-xl bg-emerald-50 px-3.5 py-2.5 text-sm font-medium text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400"
        >
          {{ resentMessage }}
        </p>

        <!-- Кнопка подтверждения -->
        <button
          type="submit"
          :disabled="loading || code.length < 6"
          class="w-full rounded-xl bg-gradient-to-br from-brand-600 to-brand-700 py-3 font-semibold text-white shadow-glow transition-all hover:from-brand-500 hover:to-brand-600 active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ loading ? t('auth.pleaseWait') : t('verify.confirmButton') }}
        </button>
      </form>

      <!-- Альтернатива: получить код в Telegram (если бот настроен) -->
      <div v-if="telegramLink" class="mt-6">
        <div class="mb-4 flex items-center gap-3">
          <span class="flex-grow border-t border-ink-200 dark:border-ink-800"></span>
          <span class="text-sm text-ink-400 dark:text-ink-500">{{ t('verify.or') }}</span>
          <span class="flex-grow border-t border-ink-200 dark:border-ink-800"></span>
        </div>
        <a
          :href="telegramLink"
          target="_blank"
          rel="noopener"
          class="flex w-full items-center justify-center gap-2 rounded-xl border border-ink-200 bg-white py-3 font-semibold text-ink-700 transition-colors hover:border-brand-300 hover:bg-brand-50 hover:text-brand-700 dark:border-ink-700 dark:bg-ink-800 dark:text-ink-200 dark:hover:border-brand-500/40 dark:hover:bg-brand-500/10 dark:hover:text-brand-300"
        >
          <svg class="h-5 w-5 text-[#229ED9]" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z" />
          </svg>
          {{ t('verify.telegramButton') }}
        </a>
      </div>

      <!-- Повторная отправка кода -->
      <p class="mt-6 text-center text-sm text-ink-500 dark:text-ink-400">
        {{ t('verify.didNotReceive') }}
        <button
          class="ml-1 font-semibold text-brand-700 hover:underline disabled:opacity-50 dark:text-brand-300"
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
