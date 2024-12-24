<script setup lang="ts">
import {onMounted, reactive, ref} from "vue";
import apiClient from '@/axios';
import {getFriends, addFriend, deleteFriend} from "@api/user.ts";
import {
  createRoom,
  getRoomMembers,
  getRoomMessages,
  getRooms,
  changeRoomName,
  addFriendToRoom,
  leaveFromRoom
} from "@api/room.ts";
import {
  createServer,
  getServers,
  getServerRooms,
  createServerRoom,
  renameServerRoom,
  deleteServerRoom,
  leaveFromServer,
  deleteServer,
  updateServer,
  joinServer, getServerMembers
} from "@api/server.ts";
import Notifications from "@/components/Notifications.vue";
import FriendField from "@/components/FriendField.vue";
import RoomModal from "@/components/RoomModal.vue";
import RoomField from "@/components/RoomField.vue";
import ServerModal from "@/components/ServerModal.vue";
import ServerField from "@/components/ServerField.vue";
import ServerRoomField from "@/components/ServerRoomField.vue";
import ServerRoomModal from "@/components/ServerRoomModal.vue";
import RoomSettingsModal from "@/components/RoomSettingsModal.vue";

const CHUNK = 500;

let audioContext: AudioContext | null = null;
let mediaStream: MediaStream | null = null;
let mediaRecorder: MediaRecorder | null = null;
let socket: WebSocket | null = null;

let token: string | null = null;
const userData = reactive({
  default_avatar_id: '0/0-0',
  login: '',
});

const isConnected = ref(false);
const isConnectedVoice = ref(false);
const textMessage = ref("");

const cur_room_id = ref(1);

const messages = ref([]);
const friends = ref([]);
const servers = ref([]);
const rooms = ref([]);
const serverRooms = ref([]);
const roomUsers = ref([]);

const currentServer = ref(null);
const isOwner = ref(false);
const selectedIndex = ref(-1);

const newFriend = ref("");
const newServer = ref("");
const notifications = ref(null);
const rmodal = ref(null);
const smodal = ref(null);
const srmodal = ref(null);
const roomSettingsModal = ref(null);
const messagesContainer = ref(null);

async function connectVoice() {
  isConnectedVoice.value = true;
  audioContext = new AudioContext();
  mediaStream = await navigator.mediaDevices.getUserMedia({audio: true});
  mediaRecorder = new MediaRecorder(mediaStream);

  mediaRecorder.ondataavailable = async (event: BlobEvent) => {
    if (event.data.size > 0) {
      await event.data.arrayBuffer().then(
          (buffer) => {
            if (socket?.readyState == WebSocket.OPEN) {
              socket?.send(buffer);
              mediaRecorder?.stop();
              mediaRecorder?.start(CHUNK);
            }
          }
      );
    }
  };
  mediaRecorder?.start(CHUNK);
}

async function initAudio(): Promise<void> {
  isConnected.value = true;
  socket = new WebSocket(`ws://${import.meta.env.VITE_API_URL}/ws/${import.meta.env.VITE_ROOM_URL}/${cur_room_id.value}/`);
  socket.binaryType = 'arraybuffer';

  socket.onmessage = (event: MessageEvent) => {
    if (typeof event.data === 'string') {
      handleTextMessage(event.data);
    } else if (isConnectedVoice && event.data instanceof ArrayBuffer) {
      const arrayBuffer = event.data as ArrayBuffer;
      audioContext?.decodeAudioData(arrayBuffer, (buffer: AudioBuffer) => {
        const source = audioContext?.createBufferSource();
        if (source) {
          source.buffer = buffer;
          source.connect(audioContext?.destination as AudioNode);
          source.start();
        }
      });
    }
  };
}

async function connect(roomID: number): Promise<void> {
  await disconnectVoice();
  cur_room_id.value = roomID;
  await getMessageHistory(roomID);
  await initAudio();
  console.log('Запись началась');
}

async function disconnectVoice(): Promise<void> {
  isConnectedVoice.value = false;
  mediaRecorder?.stop();
  mediaStream?.getTracks().forEach((track) => track.stop());

  mediaRecorder = null;
  mediaStream = null;

  console.log('Запись закончилась');
}

function handleTextMessage(message: string): void {
  console.log('Получено сообщение:', message);
  messages.value.push(JSON.parse(message));
  scrollToBottom();
}

const scrollToBottom = () => {
  setTimeout(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  }, 0);
};

async function sendTextMessage(): Promise<void> {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({
      type: "text_message",
      data: textMessage.value,
      username: userData.login
    }));
  } else {
    console.error('WebSocket не подключен или не готов для отправки сообщений.');
  }
  textMessage.value = "";
}

async function getUserInfo(): Promise<object | null> {
  try {
    token = localStorage.getItem("token");
    return (await fetch('https://login.yandex.ru/info', {
      method: 'GET',
      headers: {
        'Authorization': `OAuth ${token}`,
        'Accept': 'application/json'
      }
    })).json();
  } catch (error) {
    console.error('Error fetching user info:', error);
    return null;
  }
}

async function authDRF(login: string, image_url: string): Promise<void> {
  const response = await apiClient.post('auth', {login, image_url});
  localStorage.setItem("authToken", response.data.token);
}

async function getCurServerRooms(serverID: number) {
  await getCurServerUsers(serverID);
  const response = await getServerRooms(serverID);
  serverRooms.value = response.data;
  currentServer.value = servers.value.find(server => server.id === serverID);
  isOwner.value = currentServer.value?.owner_username === userData.login;
}

async function getCurServerUsers(serverID: number) {
  const response = await getServerMembers(serverID);
  roomUsers.value = response.data;
}

async function getMessageHistory(roomID: number) {
  const response = await getRoomMessages(roomID);
  messages.value = response.data.reverse();
  scrollToBottom();
}

async function findFriend() {
  if (newFriend.value.length > 0) {
    const response = await addFriend(newFriend.value);
    notifications.value.addNotification(response.data);
    await updateFriends();
    newFriend.value = "";
  }
}

async function findServer() {
  if (newServer.value.length > 0) {
    const response = await joinServer(newServer.value);
    notifications.value.addNotification(response.data);
    await updateServers();
    newServer.value = "";
  }
}

async function updateFriends() {
  friends.value = [];
  const response = await getFriends();
  friends.value = response.data;
}

async function deleteMyFriend(friend: string) {
  const response = await deleteFriend(friend);
  notifications.value.addNotification(response.data);
  await updateFriends();
}

function handleContentSwitch(index: number) {
  selectedIndex.value = index;
}

function showRoomModal() {
  rmodal.value.showModal();
}

function showServerModal() {
  smodal.value.showModal();
}

function showServerRoomModal() {
  srmodal.value.showModal();
}

async function createMyRoom(roomName: string) {
  console.log(roomName)
  await createRoom(roomName);
  await updateRooms();
}

async function createMyServer(name: string, image: File | null) {
  console.log(name)
  try {
    await createServer(name, image);
    notifications.value.addNotification({success: "Сервер создан."});
  } catch (error: any) {
    let errorMessage = error.response?.data?.name?.[0] || "Произошла ошибка при создании сервера.";
    notifications.value.addNotification({error: errorMessage});
  }
  await updateServers();
}

async function updateMyServer(serverId: number, updateData: { name: string, image: File | null }) {
  console.log(`Обновление сервера ${serverId}`);
  try {
    await updateServer(serverId, updateData.name, updateData.image);
    notifications.value.addNotification({success: "Сервер обновлен."});
  } catch (error: any) {
    let errorMessage = error.response?.data?.name?.[0] || "Произошла ошибка при обновлении сервера.";
    notifications.value.addNotification({error: errorMessage});
  }
  await updateServers();
}

async function deleteMyServer(serverId: number) {
  console.log(`Удаление сервера ${serverId}`);
  await deleteServer(serverId);
  notifications.value.addNotification({success: "Сервер удален."});
  await updateServers();
  serverRooms.value.length = 0;
  currentServer.value = null;
  isOwner.value = false;
}

async function createChannel(roomName: string) {
  await createServerRoom(currentServer.value.id, roomName);
  await getCurServerRooms(currentServer.value.id);
}

async function renameMyServerRoom(serverId: number, roomId: number, newName: string) {
  console.log(`Переименование канала ${roomId} на "${newName}" на сервере "${serverId}"`);
  await renameServerRoom(serverId, roomId, newName);
  await getCurServerRooms(serverId);
}

async function deleteMyServerRoom(serverId: number, roomId: number) {
  console.log(`Удаление канала ${roomId}`);
  await deleteServerRoom(serverId, roomId);
  await getCurServerRooms(serverId);
}

async function updateRooms() {
  const response = await getRooms();
  rooms.value = response.data;
}

async function updateServers() {
  const response = await getServers();
  servers.value = response.data;
}

function showRoomSettings(id: number, name: string) {
  roomSettingsModal.value.showModal(id, name);
}

async function changeMyRoomName(id: number, name: string) {
  const response = await changeRoomName(id, name);
  notifications.value.addNotification(response.data);
  await updateRooms();
}

async function addFriendToMyRoom(id: number, friendName: string) {
  const response = await addFriendToRoom(id, friendName);
  notifications.value.addNotification(response.data);
}

async function leaveFromMyRoom(id: number) {
  const response = await leaveFromRoom(id);
  notifications.value.addNotification(response.data);
  await updateRooms();
}

async function leaveServer(serverId: number) {
  console.log(`Покидание сервера ${serverId}`);
  await leaveFromServer(serverId);
  notifications.value.addNotification({success: "Сервер покинут."});
  await updateServers();
  serverRooms.value.length = 0;
  currentServer.value = null;
  isOwner.value = false;
}

async function getMyRoomMembers(roomId: number) {
  const response = await getRoomMembers(roomId);
  console.log(response.data);
  roomUsers.value = response.data;
}

onMounted(async () => {
  window.history.replaceState({}, document.title, window.location.pathname);
  const data = await getUserInfo();
  if (data) {
    Object.assign(userData, data);
    await authDRF(data.login, data.default_avatar_id);
    await updateFriends();
    await updateRooms();
    await updateServers();
  }
});
</script>

<template>
  <div class="app">
    <Notifications ref="notifications"/>
    <RoomModal ref="rmodal" :on-create="createMyRoom"/>
    <ServerModal ref="smodal" :on-create="createMyServer"/>
    <ServerRoomModal ref="srmodal"
                     @update-server="updateMyServer(currentServer.id, $event)"
                     @delete-server="deleteMyServer(currentServer.id)"
                     @create-channel="createChannel($event)"
    />
    <RoomSettingsModal ref="roomSettingsModal" :on-leave="leaveFromMyRoom" :on-add-friend="addFriendToMyRoom"
                       :on-change-name="changeMyRoomName"/>
    <header class="header">
      <div class="header__left">Ruscord</div>
      <div class="header__right">
        <span class="header__username">{{ userData.login }}</span>
        <img :src="`https://avatars.yandex.net/get-yapic/${userData.default_avatar_id}/islands-retina-middle`"
             alt="Avatar" class="header__avatar"/>
      </div>
    </header>
    <div class="main">
      <div class="sidebar">
        <cv-content-switcher aria-label='Choose content' @selected="handleContentSwitch" id="main">
          <cv-content-switcher-button owner-id="content-1" :selected="selectedIndex === 0" parent-switcher="main">
            Друзья
          </cv-content-switcher-button>
          <cv-content-switcher-button owner-id="content-2" :selected="selectedIndex === 1" parent-switcher="main">
            Сервера
          </cv-content-switcher-button>
        </cv-content-switcher>
        <section style="margin: 10px 0; max-height: calc(100vh - 120px); overflow-y: auto;">
          <cv-content-switcher-content parent-switcher="main" owner-id="content-1">
            <cv-search :placeholder="'Найти друзей'" @input="" @keyup.enter="findFriend"
                       v-model="newFriend" class="search"></cv-search>
            <FriendField v-for="friend in friends" :friend="friend.username" :friend-image="friend.image" :delete-friend="deleteMyFriend"/>
          </cv-content-switcher-content>
          <cv-content-switcher-content parent-switcher="main" owner-id="content-2">
            <cv-search :placeholder="'Найти сервер'" @input="" @keyup.enter="findServer"
                       v-model="newServer" class="search"></cv-search>
            <ServerField v-for="server in servers" :server="server" :getServerRooms="getCurServerRooms"/>
            <cv-button @click="showServerModal" class="sidebar-item primary" kind="primary" default="Primary">Создать
              сервер
            </cv-button>
          </cv-content-switcher-content>
        </section>
      </div>
      <div class="content">
        <div class="chat-sidebar">
          <cv-content-switcher-content parent-switcher="main" owner-id="content-1">
            <RoomField v-for="room in rooms" :id="room.id" :name="room.name" :connect="connect"
                       :show-settings="showRoomSettings" :room-member="getMyRoomMembers"/>
            <cv-button @click="showRoomModal" class="sidebar-item primary" kind="primary" default="Primary">Создать
              комнату
            </cv-button>
          </cv-content-switcher-content>
          <cv-content-switcher-content parent-switcher="main" owner-id="content-2">
            <ServerRoomField v-for="room in serverRooms" :id="room.id" :name="room.name"
                             :connect="connect" :isOwner="isOwner"
                             @rename-room="renameMyServerRoom(currentServer.id, room.id, $event)"
                             @delete-room="deleteMyServerRoom(currentServer.id, room.id)"/>

            <cv-button v-if="isOwner && currentServer"
                       @click="showServerRoomModal" class="sidebar-item primary" kind="primary">
              Управление сервером
            </cv-button>
            <cv-button
                v-if="!isOwner && currentServer"
                @click="leaveServer(currentServer.id)"
                class="sidebar-item danger"
                kind="danger"
            >
              Покинуть сервер
            </cv-button>
          </cv-content-switcher-content>
        </div>
        <div class="chat">
          <div class="chat__messages" ref="messagesContainer">
            <div v-for="message in messages" class="chat__message">
              <strong>{{ message.username }}:</strong> {{ message.message }}
            </div>
          </div>
          <div class="chat__input">
            <input
                v-model="textMessage"
                @keyup.enter="sendTextMessage"
                type="text"
                placeholder="Введите сообщение..."
                class="chat__input-field"
            />
            <button @click="sendTextMessage" class="chat__send-button">Отправить</button>
          </div>
        </div>
        <div v-if="roomUsers.length" class="right-sidebar">
          <div v-if="isConnected">
            <cv-button v-if="isConnectedVoice" @click="disconnectVoice" class="sidebar-item danger" kind="danger">Отключиться</cv-button>
            <cv-button v-else @click="connectVoice" class="sidebar-item primary" kind="primary">Подключиться</cv-button>
          </div>
          <div class="right-sidebar__users">
            <FriendField v-for="user in roomUsers" :friend="user.username" :friend-image="user.image"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
* {
  color: white;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
}

.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #202225;
  font-size: 20px;
}

.header__left {
  font-weight: bold;
}

.header__right {
  display: flex;
  align-items: center;
}

.header__avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-left: 10px;
}

.header__username {
  font-size: 16px;
}

.main {
  display: flex;
  flex: 1;
  background-color: #2f3136;
  height: 90vh;
}

.sidebar {
  width: 280px;
  background-color: #202225;
}

.content {
  display: flex;
  flex: 1;
}

.chat-sidebar {
  width: 280px;
  background-color: #292b2f;
  overflow-y: auto;
  overflow-x: hidden;
  padding-top: 10px;
  padding-bottom: 10px;
}

.chat {
  display: flex;
  flex-direction: column;
  flex: 1;
  background-color: #36393f;
  color: white;
  padding: 20px;
}

.chat__messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
}

.chat__message {
  margin-bottom: 10px;
}

.chat__input {
  display: flex;
  align-items: center;
}

.chat__input-field {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #40444b;
  color: white;
  margin-right: 10px;
}

.chat__send-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #7289da;
  color: white;
  cursor: pointer;
}

.chat__send-button:hover {
  background-color: #677bc4;
}

.sidebar-item {
  width: 100%;
  margin: 10px;
}

.primary {
  border-radius: 3px;
  background-color: #7289da;
  margin: 10px;
  width: calc(100% - 20px);
}

.danger {
  background-color: #df3d3d;
  border-radius: 3px;
  margin: 10px;
  width: calc(100% - 20px);
}
.right-sidebar {
  width: 270px;
  background-color: #2c2f33;
  color: white;
  padding: 10px;
}

.right-sidebar__connect-button {
  width: 100%;
  margin-bottom: 10px;
}

.right-sidebar__users {
  display: flex;
  flex-direction: column;
}

::-webkit-scrollbar{
  width: 10px;
}
::-webkit-scrollbar-track{
  background: #2c2f33;
  border-radius: 5px;
}
::-webkit-scrollbar-thumb{
  background: #7289da;
  border-radius: 12px;
  transition: all 0.3s ease;
}
::-webkit-scrollbar-thumb:hover{
  background: #677bc4;
}
</style>