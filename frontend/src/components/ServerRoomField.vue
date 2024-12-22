<script setup lang="ts">
const props = defineProps<{
  id: number;
  name: string;
  connect: (id: number) => void;
}>();

function handleClick() {
  props.connect(props.id);
}
</script>

<template>
  <div class="server-room-field" @click="handleClick">
    <cv-button class="room-button" kind="secondary" default="Primary">{{ name }}</cv-button>
  </div>
</template>

<style scoped>
.server-room-field {
  display: flex;
  align-items: center;
  margin: 10px;
  width: calc(100% - 20px);
  background-color: #36393f;
  border-radius: 3px;
}

.room-button {
  flex-grow: 1;
  text-align: left;
  background: 0;
}
</style>
