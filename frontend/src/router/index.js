// frontend/src/router/index.js
/**
 * Конфигурация Vue Router.
 * Определяет маршруты приложения и связывает их с компонентами.
 */

import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import ProductDetailPage from '@/views/ProductDetailPage.vue'
import CartPage from '@/views/CartPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import VerifyPage from '@/views/VerifyPage.vue'
import i18n from '@/i18n'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
      meta: {
        titleKey: 'titles.home',
      },
    },
    {
      path: '/product/:id',
      name: 'product-detail',
      component: ProductDetailPage,
      meta: {
        titleKey: 'titles.product',
      },
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartPage,
      meta: {
        titleKey: 'titles.cart',
      },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: {
        titleKey: 'titles.login',
      },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage,
      meta: {
        titleKey: 'titles.register',
      },
    },
    {
      path: '/verify',
      name: 'verify',
      component: VerifyPage,
      meta: {
        titleKey: 'titles.verify',
      },
    },
  ],
  // Прокрутка страницы вверх при переходе между роутами
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

// Обновление заголовка страницы при навигации
router.beforeEach((to, from, next) => {
  const { t } = i18n.global
  document.title = to.meta.titleKey ? t(to.meta.titleKey) : 'FastAPI Shop'
  next()
})

export default router
