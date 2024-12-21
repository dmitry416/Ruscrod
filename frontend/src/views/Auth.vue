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
  <div class="container">
    <img src="@/images/logo.webp" alt="" class="logo--image">
    <button class="button--in" @click="loginWithYandex">Войти через Яндекс</button>
  </div>
</template>

<style scoped>
.container {
  background-color: #2f3136;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.logo--image {
  max-width: 200px;
  height: auto;
  margin-bottom: 80px;
}

.button--in {
  background-color: #FF0000;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: fit-content;
  height: 50px;
}

.button--in:hover {
  background-color: #CC0000;
}
</style>