<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import heroImage from './assets/hero.png'

const user = ref(null)
const isTelegramEnv = ref(false)
const theme = ref({
  accent: '#6ee7b7',
  surface: '#111827',
  text: '#f8fafc',
})

const highlights = [
  {
    label: 'Drop this week',
    value: '12 AI tools',
    note: 'Curated access with fast delivery',
  },
  {
    label: 'Support',
    value: '24/7 online',
    note: 'Telegram-first help without tickets',
  },
  {
    label: 'Average activation',
    value: 'under 3 min',
    note: 'After payment confirmation',
  },
]

const categories = [
  {
    name: 'AI Workspace',
    description: 'Premium assistants, copilots and research stacks.',
    badge: 'Fast launch',
  },
  {
    name: 'Creative Suite',
    description: 'Visual tools, generative media and design boosters.',
    badge: 'Hot today',
  },
  {
    name: 'Private Setup',
    description: 'VPN, accounts and secure digital bundles for teams.',
    badge: 'Verified',
  },
]

const featured = [
  {
    title: 'Nox Prime Pack',
    price: '$19',
    caption: 'AI starter bundle for daily work and study.',
  },
  {
    title: 'Creator Stack',
    price: '$27',
    caption: 'Visual generation and editing tools in one flow.',
  },
]

const timeline = [
  'Open the showcase inside Telegram.',
  'Choose a category and confirm the order.',
  'Receive access details directly in chat.',
]

let tg = null
let handleMainButtonClick = null

const welcomeText = computed(() => {
  if (user.value?.first_name) {
    return `Welcome back, ${user.value.first_name}. Your next digital drop is ready.`
  }

  if (isTelegramEnv.value) {
    return 'Telegram is connected. Authorize once and unlock the catalog in one tap.'
  }

  return 'Open this page from the bot to use payments, delivery status and instant actions.'
})

onMounted(() => {
  tg = window.Telegram?.WebApp ?? null

  if (!tg) {
    return
  }

  isTelegramEnv.value = true
  tg.ready()
  tg.expand()

  user.value = tg.initDataUnsafe?.user ?? null

  const tgTheme = tg.themeParams ?? {}
  theme.value = {
    accent: tgTheme.button_color || '#6ee7b7',
    surface: tgTheme.secondary_bg_color || '#111827',
    text: tgTheme.text_color || '#f8fafc',
  }

  tg.MainButton.setText('Open catalog')
  tg.MainButton.show()

  handleMainButtonClick = () => {
    tg.sendData(
      JSON.stringify({
        action: 'open_catalog',
        source: 'miniapp',
        time: Date.now(),
      }),
    )
  }

  tg.onEvent('mainButtonClicked', handleMainButtonClick)
})

onUnmounted(() => {
  if (tg && handleMainButtonClick) {
    tg.offEvent('mainButtonClicked', handleMainButtonClick)
  }
})
</script>

<template>
  <main
    class="app-shell"
    :style="{
      '--accent': theme.accent,
      '--surface': theme.surface,
      '--text': theme.text,
    }"
  >
    <div class="ambient ambient-left"></div>
    <div class="ambient ambient-right"></div>

    <section class="hero-card">
      <div class="hero-copy">
        <p class="eyebrow">Arvexo mini app</p>
        <h1>Digital storefront built for Telegram speed.</h1>
        <p class="hero-text">
          {{ welcomeText }}
        </p>

        <div class="hero-actions">
          <button class="primary-button" type="button">
            Explore drops
          </button>
          <button class="ghost-button" type="button">
            Delivery policy
          </button>
        </div>

        <div class="telegram-pill">
          <span class="status-dot"></span>
          <span v-if="isTelegramEnv">Connected to Telegram WebApp</span>
          <span v-else>Preview mode outside Telegram</span>
        </div>
      </div>

      <div class="hero-visual">
        <div class="visual-frame">
          <img :src="heroImage" alt="Arvexo platform illustration" />
        </div>
        <div class="visual-card">
          <span>Live now</span>
          <strong>Instant delivery after payment</strong>
        </div>
      </div>
    </section>

    <section class="stats-grid">
      <article
        v-for="item in highlights"
        :key="item.label"
        class="stat-card"
      >
        <p>{{ item.label }}</p>
        <strong>{{ item.value }}</strong>
        <span>{{ item.note }}</span>
      </article>
    </section>

    <section class="content-grid">
      <article class="panel panel-large">
        <div class="panel-heading">
          <p class="eyebrow">Featured categories</p>
          <h2>Designed like a boutique, not a file dump.</h2>
        </div>

        <div class="category-list">
          <div
            v-for="category in categories"
            :key="category.name"
            class="category-card"
          >
            <span class="badge">{{ category.badge }}</span>
            <h3>{{ category.name }}</h3>
            <p>{{ category.description }}</p>
          </div>
        </div>
      </article>

      <article class="panel">
        <div class="panel-heading">
          <p class="eyebrow">Featured offers</p>
          <h2>Compact premium cards.</h2>
        </div>

        <div class="offer-list">
          <div
            v-for="offer in featured"
            :key="offer.title"
            class="offer-card"
          >
            <div>
              <h3>{{ offer.title }}</h3>
              <p>{{ offer.caption }}</p>
            </div>
            <strong>{{ offer.price }}</strong>
          </div>
        </div>
      </article>
    </section>

    <section class="panel timeline-panel">
      <div class="panel-heading">
        <p class="eyebrow">Flow</p>
        <h2>Three moves from browse to delivery.</h2>
      </div>

      <div class="timeline">
        <div
          v-for="(step, index) in timeline"
          :key="step"
          class="timeline-step"
        >
          <span>{{ `0${index + 1}` }}</span>
          <p>{{ step }}</p>
        </div>
      </div>
    </section>
  </main>
</template>
