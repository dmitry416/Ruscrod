<script setup lang="ts">
import '@carbon/icons-vue'

const props = defineProps<{
  id: number;
  name: string;
  connect: (id: number) => void;
  showSettings: (id: number, name: string) => void;
}>();
</script>

<template>
  <div class="container">
    <cv-button class="room-button" kind="secondary" default="Primary">
      <span @click="props.connect(id)" class="room-name">{{ name }}</span>
      <cv-icon-button @click="props.showSettings(id, name)" label="Настройки" size="field" icon="Settings20"
                      class="icon-right"/>
    </cv-button>
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

.room-button {
  display: flex;
  align-items: center;
  width: 100%;
  text-align: left;
  background: 0;
  border: none;
  padding: 0 0 0 15px;
}

.icon-right {
  margin-left: auto;
  margin-right: 10px;
  border-radius: 100%;
  background-color: #7289da;
}

.room-name {
  flex-grow: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>