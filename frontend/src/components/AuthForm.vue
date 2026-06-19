<!-- frontend/src/components/AuthForm.vue -->
<!--
  Переиспользуемая форма аутентификации.
  Режим (вход/регистрация) задаётся пропом mode.
-->

<template>
  <div class="min-h-screen bg-white flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md">
      <!-- Заголовок -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-extrabold text-black mb-2">
          {{ isLogin ? t('auth.signInTitle') : t('auth.signUpTitle') }}
        </h1>
        <p class="text-gray-500">
          {{ isLogin ? t('auth.signInWelcome') : t('auth.signUpWelcome') }}
        </p>
      </div>

      <!-- Форма -->
      <form class="space-y-4 border-2 border-black rounded-lg p-8" @submit.prevent="handleSubmit">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('auth.email') }}</label>
          <input
            v-model="email"
            type="email"
            required
            autocomplete="email"
            class="w-full border-2 border-gray-300 rounded-md px-3 py-2 text-black placeholder-gray-400 focus:border-black focus:outline-none"
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
          <p v-if="passwordsMismatch" class="mt-1 text-sm text-red-600">
            {{ t('auth.passwordsDontMatch') }}
          </p>
        </div>

        <!-- Сообщение об ошибке -->
        <p v-if="error" class="text-sm text-red-600">{{ error }}</p>

        <!-- Кнопка отправки -->
        <button
          type="submit"
          :disabled="loading || passwordsMismatch"
          class="w-full bg-black text-white font-semibold py-2.5 rounded-md hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? t('auth.pleaseWait') : isLogin ? t('auth.signInButton') : t('auth.createAccount') }}
        </button>
      </form>

      <!-- Перекрёстная ссылка на второй режим -->
      <p class="text-center text-sm text-gray-600 mt-6">
        <template v-if="isLogin">
          {{ t('auth.noAccount') }}
          <router-link to="/register" class="text-black font-semibold hover:underline ml-1">
            {{ t('auth.register') }}
          </router-link>
        </template>
        <template v-else>
          {{ t('auth.haveAccount') }}
          <router-link to="/login" class="text-black font-semibold hover:underline ml-1">
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
      await authStore.register(email.value, password.value)
      router.push({ name: 'verify', query: { email: email.value } })
    }
  } catch (err) {
    // Почта не подтверждена (403) — ведём на экран ввода кода
    if (isLogin.value && err.response?.status === 403) {
      router.push({ name: 'verify', query: { email: email.value } })
      return
    }
    error.value = resolveAuthError(err, isLogin.value)
  } finally {
    loading.value = false
  }
}
</script>
