<script setup lang="ts">
const props = defineProps<{
  server: {
    id: number;
    name: string;
    image: string | null;
  };
  getServerRooms: (serverId: number) => void;
}>();

function handleClick() {
  props.getServerRooms(props.server.id);
}
</script>

<template>
  <div class="server-field" @click="handleClick">
    <img :src="server.image" alt="Server Avatar" class="server-avatar" v-if="server.image" />
    <cv-button class="server-button" kind="secondary" default="Primary">{{ server.name }}</cv-button>
  </div>
</template>

<style scoped>
.server-field {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  width: 100%;
}

.server-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}

.server-button {
  flex-grow: 1;
  text-align: left;
}
</style>