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
    <cv-button class="server-button" kind="secondary">
      <img :src="server.image" alt="Server Avatar" class="server-avatar" v-if="server.image" />
      <span class="server-name">{{ server.name }}</span>
    </cv-button>
  </div>
</template>

<style scoped>
.server-field {
  display: flex;
  align-items: center;
  margin: 10px;
  width: calc(100% - 20px);
  background-color: #36393f;
  border-radius: 3px;
  cursor: pointer;
}

.server-button {
  display: flex;
  align-items: center;
  width: 100%;
  text-align: left;
  background: 0;
  border: none;
  padding: 0 10px;
}

.server-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}

.server-name {
  flex-grow: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>