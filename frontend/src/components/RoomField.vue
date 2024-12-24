<script setup lang="ts">
import '@carbon/icons-vue'

const props = defineProps<{
  id: number;
  name: string;
  connect: (id: number) => void;
  roomMember: (id: number) => void;
  showSettings: (id: number, name: string) => void;
}>();
</script>

<template>
  <div class="container">
    <cv-button class="room-button" kind="secondary" default="Primary">
      <span @click="props.connect(id);props.roomMember(id);" class="room-name">{{ name }}</span>
      <img @click="props.showSettings(id, name)" src="/settings.svg" class="icon-right"/>
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
  width: 40px;
  padding: 5px;
}

.room-name {
  flex-grow: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>