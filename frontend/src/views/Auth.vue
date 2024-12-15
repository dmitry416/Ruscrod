<script lang="ts">
import {YANDEX_CLIENT_ID, YANDEX_REDIRECT} from "@/config.ts";

export default {
  methods: {
    loginWithYandex() {
      window.location.href = `https://oauth.yandex.ru/authorize?response_type=code&client_id=${YANDEX_CLIENT_ID}&redirect_uri=${YANDEX_REDIRECT}`;
    }
  }
}
</script>

<template>
  <div>
    <button @click="loginWithYandex">Войти через Яндекс</button>
  </div>
</template>
