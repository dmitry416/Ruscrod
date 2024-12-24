<script setup lang="ts">
import {ref} from 'vue';

const props = defineProps<{
  friend: string;
  friendImage: string;
  deleteFriend?: (friend: string) => void;
}>();

const isSelected = ref(false);

</script>

<template>
  <div class="friend-field">
    <cv-button @click="isSelected = !isSelected" class="friend-button" kind="secondary" default="Primary">
      <img :src="`https://avatars.yandex.net/get-yapic/${friendImage}/islands-retina-middle`" alt="User Avatar" class="user-avatar" />
      <span class="user-name">{{friend}}</span>
    </cv-button>
    <cv-button v-if="isSelected && deleteFriend" @click="props.deleteFriend(friend)" kind="danger" class="friend-button delete">Удалить из друзей</cv-button>
  </div>
</template>

<style scoped>
.friend-field {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin: 10px;
  width: calc(100% - 20px);
  border-radius: 3px;
}

.friend-button {
  width: 100%;
  border-radius: 3px;
  background-color: #36393f;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}

.user-name {
  flex-grow: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delete {
  margin-top: 10px;
  background-color: #df3d3d
}
</style>