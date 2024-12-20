<script setup lang="ts">
import {ref} from 'vue';

const props = defineProps<{
  friend: string;
  deleteFriend: (friend: string) => void;
}>();

const isSelected = ref(false);

</script>

<template>
  <div class="friend-field">
    <cv-button @click="isSelected = !isSelected" class="friend-button" kind="secondary" default="Primary">{{friend}}</cv-button>
    <cv-button v-if="isSelected" @click="props.deleteFriend(friend)" kind="danger" class="friend-button">Удалить из друзей</cv-button>
  </div>
</template>

<style scoped>
.friend-field {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 10px;
}

.friend-button {
  width: 100%;
}
</style>