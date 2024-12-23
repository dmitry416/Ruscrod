<script setup lang="ts">
import '@carbon/icons-vue'
import { ref } from 'vue';

const props = defineProps<{
  id: number;
  name: string;
  connect: (id: number) => void;
  isOwner: boolean;
}>();

const emit = defineEmits<{
  (e: 'rename-room', newName: string): void;
  (e: 'delete-room'): void;
}>();

const isSettingsVisible = ref(false);
const localName = ref(props.name);

function handleClick() {
  props.connect(props.id);
}

function showSettings() {
  localName.value = props.name;
  isSettingsVisible.value = true;
}

function hideSettings() {
  isSettingsVisible.value = false;
}

function deleteRoom() {
  emit('delete-room');
  hideSettings();
}

function renameRoom() {
  emit('rename-room', localName.value);
  hideSettings();
}
</script>

<template>
  <div class="server-room-field">
    <cv-button @click="handleClick" class="room-button" kind="secondary" default="Primary">{{ name }}</cv-button>
    <cv-icon-button v-if="isOwner" @click="showSettings" label="Настройки" size="field" icon="Settings20" class="icon-right"/>
  </div>

  <cv-modal :visible="isSettingsVisible" @modal-hide-request="hideSettings" @modal-hidden="hideSettings">
    <template v-slot:title>Настройки канала</template>
    <template v-slot:content>
      <cv-text-input
        label="Название канала"
        placeholder="Введите новое название"
        v-model="localName"
        class="input-field"
      />

      <div class="button-group">
        <cv-button @click="renameRoom" kind="primary" class="save-button">Сохранить изменения</cv-button>
        <cv-button @click="deleteRoom" kind="danger" class="delete-button">Удалить канал</cv-button>
      </div>
    </template>
  </cv-modal>
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

.icon-right {
  margin-left: auto;
  margin-right: 10px;
  border-radius: 100%;
  background-color: #7289da;
}

.input-field {
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.save-button, .delete-button {
  flex-grow: 1;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.save-button {
  background-color: #7289da;
  color: white;
}

.delete-button {
  background-color: #ff5252;
  color: white;
}
</style>