<script setup lang="ts">
import '@carbon/icons-vue'
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
    <cv-icon-button @click="showSettings" label="Настройки" size="field" icon="Settings20" class="icon-right"/>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  align-items: center;
  margin: 10px;
  width: calc(100% - 20px);
  background-color: #36393f;
  border-radius: 3px;
}

.icon-right {
  margin-left: auto;
  margin-right: 10px;
  border-radius: 100%;
  background-color: #7289da;
}

.sidebar-item {
  width: 80%;
  background: 0;
}
</style>