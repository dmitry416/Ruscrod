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
  margin-bottom: 10px;
  width: 100%;
}

.room-button {
  flex-grow: 1;
  text-align: left;
}
</style>
