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
    <div class="header">Ruscord</div>
    <div class="place">
      <img src="@/images/logo.webp" alt="" class="logo--image">
      <button class="button--in" @click="loginWithYandex">Войти через Яндекс</button>
    </div>
  </div>
</template>

<style scoped>
.container {
  background-color: #36393f;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.place {
  border-radius: 5px;
  background-color: #2f3136;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 70vh;
  width: 100vh;
}

.header {
  text-align: center;
  position: absolute;
  top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 20px;
  background-color: #202225;
  font-size: 28px;
  width: 100%;
  color: white;
  font-weight: bold;
  height: 50px;
}


.logo--image {
  max-width: 200px;
  height: auto;
  margin-bottom: 80px;
}

.button--in {
  background-color: #7289da;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: fit-content;
  height: 50px;
}

.button--in:hover {
  background-color: #7289da;
}
</style>