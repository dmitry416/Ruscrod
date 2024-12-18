<script lang="ts">

export default {
  methods: {
    loginWithYandex() {
      window.location.href = `https://oauth.yandex.ru/authorize?response_type=code&client_id=${import.meta.env.VITE_YANDEX_CLIENT_ID}&redirect_uri=${import.meta.env.VITE_YANDEX_REDIRECT}`;
    }
  }
}
</script>

<template>
  <div>
    <button @click="loginWithYandex">Войти через Яндекс</button>
  </div>
</template>
