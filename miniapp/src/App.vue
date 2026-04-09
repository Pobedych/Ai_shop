<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const user = ref(null)
const isTelegramEnv = ref(false)

let tg = null
let handleMainButtonClick = null

onMounted(() => {
  tg = window.Telegram?.WebApp ?? null

  if (!tg) return

  isTelegramEnv.value = true
  tg.ready()
  tg.expand()

  user.value = tg.initDataUnsafe?.user ?? null

  tg.MainButton.setText('Send data to bot')
  tg.MainButton.show()

  handleMainButtonClick = () => {
    tg.sendData(JSON.stringify({
      action: 'open_miniapp',
      time: Date.now()
    }))
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
  <div style="padding: 16px">
    <h1>NoxShop</h1>

    <p v-if="user">Привет, {{ user.first_name }}, скоро здесь будет что-то интересное.</p>
    <p v-else-if="isTelegramEnv">Приложение открыто в Telegram, но данные пользователя недоступны.</p>
    <p v-else>Открыто вне Telegram. Для полного сценария запусти Mini App из бота.</p>
  </div>
</template>
