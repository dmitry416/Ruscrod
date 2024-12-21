<script setup lang="ts">
import {ref} from 'vue';

const props = defineProps<{
  id: number;
  name: string;
  connect: (id: number) => void;
  showSettings: () => void;
}>();

</script>

<template>
  <div class="container">
    <cv-button @click="props.connect(id)" class="sidebar-item" kind="secondary" default="Primary">{{ name }}</cv-button>
    <cv-icon-button @click="showSettings" label="Настройки" size="field" icon="Bee20" class="icon-right"/>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 10px;
}

.icon-right {
  margin-left: auto;
}

.sidebar-item {
  width: 80%;
}
</style>