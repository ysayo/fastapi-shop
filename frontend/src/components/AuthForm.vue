<!-- frontend/src/components/AuthForm.vue -->
<!--
  Переиспользуемая форма аутентификации.
  Режим (вход/регистрация) задаётся пропом mode.
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
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
            />
          </svg>
        </div>
        <h1 class="text-2xl font-extrabold tracking-tight text-ink-900 dark:text-ink-50 mb-1">
          {{ isLogin ? t('auth.signInTitle') : t('auth.signUpTitle') }}
        </h1>
        <p class="text-ink-500 dark:text-ink-400">
          {{ isLogin ? t('auth.signInWelcome') : t('auth.signUpWelcome') }}
        </p>
      </div>

      <!-- Форма -->
      <form
        class="space-y-4 rounded-2xl border border-ink-200/70 bg-white p-8 shadow-card dark:border-ink-800 dark:bg-ink-900"
        @submit.prevent="handleSubmit"
      >
        <div>
          <label class="mb-1.5 block text-sm font-medium text-ink-700 dark:text-ink-200">{{ t('auth.email') }}</label>
          <input
            v-model="email"
            type="email"
            required
            autocomplete="email"
            class="w-full rounded-xl border border-ink-200 bg-ink-50 px-3.5 py-2.5 text-ink-900 placeholder-ink-400 transition-all focus:border-brand-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-800 dark:text-ink-50 dark:placeholder-ink-500 dark:focus:bg-ink-800 dark:focus:ring-brand-500/20"
            placeholder="you@example.com"
          />
        </div>

        <!-- Пароль -->
        <PasswordInput
          v-model="password"
          :label="t('auth.password')"
          :autocomplete="isLogin ? 'current-password' : 'new-password'"
        />

        <!-- Подтверждение пароля (только при регистрации) -->
        <div v-if="!isLogin">
          <PasswordInput
            v-model="confirmPassword"
            :label="t('auth.confirmPassword')"
            autocomplete="new-password"
          />
          <!-- Подсказка о несовпадении паролей -->
          <p v-if="passwordsMismatch" class="mt-1.5 text-sm text-red-600 dark:text-red-400">
            {{ t('auth.passwordsDontMatch') }}
          </p>
        </div>

        <!-- Сообщение об ошибке -->
        <p
          v-if="error"
          class="rounded-xl bg-red-50 px-3.5 py-2.5 text-sm font-medium text-red-600 dark:bg-red-500/10 dark:text-red-400"
        >
          {{ error }}
        </p>

        <!-- Кнопка отправки -->
        <button
          type="submit"
          :disabled="loading || passwordsMismatch"
          class="w-full rounded-xl bg-gradient-to-br from-brand-600 to-brand-700 py-3 font-semibold text-white shadow-glow transition-all hover:from-brand-500 hover:to-brand-600 active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ loading ? t('auth.pleaseWait') : isLogin ? t('auth.signInButton') : t('auth.createAccount') }}
        </button>
      </form>

      <!-- Перекрёстная ссылка на второй режим -->
      <p class="mt-6 text-center text-sm text-ink-500 dark:text-ink-400">
        <template v-if="isLogin">
          {{ t('auth.noAccount') }}
          <router-link to="/register" class="ml-1 font-semibold text-brand-700 hover:underline dark:text-brand-300">
            {{ t('auth.register') }}
          </router-link>
        </template>
        <template v-else>
          {{ t('auth.haveAccount') }}
          <router-link to="/login" class="ml-1 font-semibold text-brand-700 hover:underline dark:text-brand-300">
            {{ t('auth.login') }}
          </router-link>
        </template>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PasswordInput from '@/components/PasswordInput.vue'
import { useAuthErrorMessage } from '@/composables/useAuthErrorMessage'

const { t } = useI18n()
const resolveAuthError = useAuthErrorMessage()

const props = defineProps({
  mode: {
    type: String,
    required: true,
    validator: (value) => ['login', 'register'].includes(value),
  },
})

const router = useRouter()
const authStore = useAuthStore()

const isLogin = computed(() => props.mode === 'login')

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

// Пароли не совпадают (только при регистрации и когда подтверждение заполнено)
const passwordsMismatch = computed(
  () => !isLogin.value && confirmPassword.value !== '' && password.value !== confirmPassword.value,
)

/**
 * Отправить форму: войти или зарегистрироваться, затем вернуться на главную
 */
async function handleSubmit() {
  error.value = ''
  // При регистрации требуем совпадение паролей
  if (!isLogin.value && password.value !== confirmPassword.value) {
    error.value = t('auth.passwordsDontMatch')
    return
  }
  loading.value = true
  try {
    if (isLogin.value) {
      await authStore.login(email.value, password.value)
      router.push('/')
    } else {
      // После регистрации отправляем на экран ввода кода подтверждения
      const data = await authStore.register(email.value, password.value)
      router.push({
        name: 'verify',
        query: { email: email.value, tg: data?.telegram_link || undefined },
      })
    }
  } catch (err) {
    // Нужен код подтверждения (403) — ведём на экран ввода кода (с ссылкой на бота, если он настроен)
    if (isLogin.value && err.response?.status === 403) {
      router.push({
        name: 'verify',
        query: { email: email.value, tg: err.response.data?.telegram_link || undefined },
      })
      return
    }
    error.value = resolveAuthError(err, isLogin.value)
  } finally {
    loading.value = false
  }
}
</script>
