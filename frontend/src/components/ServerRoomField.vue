<script setup lang="ts">
import '@carbon/icons-vue'
import {ref} from 'vue';

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
    <cv-button class="room-button" kind="secondary" default="Primary">
      <span @click="handleClick" class="server-room-name">{{ name }}</span>
      <img v-if="isOwner" @click="showSettings" src="/settings.svg" class="icon-right"/>
<!--      <cv-icon-button v-if="isOwner" @click="showSettings" label="Настройки" size="field" icon="Settings20"-->
<!--                      class="icon-right"/>-->
    </cv-button>
  </div>

  <cv-modal
      :visible="isSettingsVisible" @modal-hide-request="hideSettings"
      @modal-hidden="hideSettings" @primary-click="renameRoom">
    >
    <template v-slot:title>Настройки канала</template>
    <template v-slot:content>
      <cv-text-input
          label="Название канала"
          placeholder="Введите новое название"
          v-model="localName"
          class="input-field"
          @keyup.enter="renameRoom"
      />

      <section style="margin: 10px 0;">
        <cv-button @click="deleteRoom" kind="danger" class="delete">Удалить канал</cv-button>
      </section>
    </template>
    <template v-slot:primary-button>Сохранить изменения</template>
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

.server-room-name {
  flex-grow: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.input-field {
  margin-bottom: 20px;
}

.delete {
  width: 100%;
  margin-top: 10px;
  background-color: #df3d3d;
  border-radius: 3px;
}
</style>