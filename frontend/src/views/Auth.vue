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
    <img src="..frontend/images/logo.webp" alt=""
         class="logo--image">
    <button class="button--in" @click="loginWithYandex">Войти через Яндекс</button>
  </div>
</template>


<style>
body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}

.logo--image {
  max-width: 200px;
  height: auto;
  margin-bottom: 20px;
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
  width: 200px;
  height: 75px;
}

.button--in:hover {
  background-color: #CC0000;
}
</style>