<script setup lang="ts">
import {onMounted, reactive, ref} from "vue";
import apiClient from '@/axios';
import {getFriends, addFriend, deleteFriend} from "@api/user.ts";
import {createRoom, getRoomMembers, getRoomMessages, getRooms} from "@api/room.ts";
import {createServer, getServers, getServerRooms, createServerRoom} from "@api/server.ts";
import Notifications from "@/components/Notifications.vue";
import FriendField from "@/components/FriendField.vue";
import RoomModal from "@/components/RoomModal.vue";
import RoomField from "@/components/RoomField.vue";
import ServerModal from "@/components/ServerModal.vue";
import ServerField from "@/components/ServerField.vue";
import ServerRoomField from "@/components/ServerRoomField.vue";
import ServerRoomModal from "@/components/ServerRoomModal.vue";

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
const textMessage = ref("");

const cur_room_id = ref(1);

const messages = ref([]);
const friends = ref([]);
const servers = ref([]);
const rooms = ref([]);
const serverRooms = ref([]);

const currentServer = ref(null);
const isOwner = ref(false);
const selectedIndex = ref(-1);

const newFriend = ref("");
const notifications = ref(null);
const rmodal = ref(null);
const smodal = ref(null);
const srmodal = ref(null);

async function initAudio(): Promise<void> {
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

  socket = new WebSocket(`ws://${import.meta.env.VITE_API_URL}/ws/${import.meta.env.VITE_ROOM_URL}/${cur_room_id.value}/`);
  socket.binaryType = 'arraybuffer';

  socket.onmessage = (event: MessageEvent) => {
    if (typeof event.data === 'string') {
      handleTextMessage(event.data);
    } else if (event.data instanceof ArrayBuffer) {
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
  cur_room_id.value = roomID;
  isConnected.value = true;
  await getMessageHistory(roomID, 1);
  await initAudio();
  mediaRecorder?.start(CHUNK);
  console.log('Запись началась');
}

async function disconnect(): Promise<void> {
  isConnected.value = false;

  mediaRecorder?.stop();
  socket?.close();
  mediaStream?.getTracks().forEach((track) => track.stop());

  mediaRecorder = null;
  socket = null;
  mediaStream = null;

  console.log('Запись закончилась');
}

function handleTextMessage(message: string): void {
  console.log('Получено сообщение:', message);
  messages.value.push(JSON.parse(message));
}

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
  const response = await getServerRooms(serverID);
  serverRooms.value = response.data;
  currentServer.value = servers.value.find(server => server.id === serverID);
  isOwner.value = currentServer.value?.owner_username === userData.login;
}

async function getMessageHistory(roomID: number, page: number) {
  const response = await getRoomMessages(roomID, page);
  messages.value = response.data.reverse();
}

async function findFriend() {
  if (newFriend.value.length > 0) {
    if (newFriend.value.length > 0) {
      const response = await addFriend(newFriend.value);
      if (response.data.error) {
        notifications.value.addNotification("error", "Ошибка", response.data.error);
      } else if (response.data.warning) {
        notifications.value.addNotification("warning", "Внимание", response.data.warning);
      } else if (response.data.success) {
        notifications.value.addNotification("success", "Успешно", response.data.success);
        await updateFriends();
      }
      newFriend.value = "";
    }
  }
}

async function updateFriends() {
  friends.value = [];
  const response = await getFriends();
  friends.value = response.data.map((friend: any) =>
      friend.user1_username === userData.login ? friend.user2_username : friend.user1_username);
}

async function deleteMyFriend(friend: string) {
  const response = await deleteFriend(friend);
  if (response.data.error) {
    notifications.value.addNotification("error", "Ошибка", response.data.error);
  } else if (response.data.success) {
    notifications.value.addNotification("success", "Успешно", response.data.success);
  }
  await updateFriends();
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
    notifications.value.addNotification("success", "Успешно", "Сервер создан.");
  } catch (error: any) {
    let errorMessage = error.response?.data?.name?.[0] || "Произошла ошибка при создании сервера.";
    notifications.value.addNotification("error", "Ошибка", errorMessage);
  }
  await updateServers();
}

async function createMyServerRoom(roomName: string) {
  if (!currentServer.value) {
    console.error("Текущий сервер не выбран");
    return;
  }

  await createServerRoom(currentServer.value.id, roomName);
  await getCurServerRooms(currentServer.value.id);
}

async function updateRooms() {
  const response = await getRooms();
  rooms.value = response.data;
}

async function updateServers() {
  const response = await getServers();
  servers.value = response.data;
}

function showRoomSettings() {
  console.log("Room settings");
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
    <ServerRoomModal ref="srmodal" :on-create="createMyServerRoom"/>
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
        <cv-content-switcher aria-label='Choose content' @selected="">
          <cv-content-switcher-button content-selector=".content-1" :selected="selectedIndex === 0">Друзья
          </cv-content-switcher-button>
          <cv-content-switcher-button content-selector=".content-2" :selected="selectedIndex === 1">Сервера
          </cv-content-switcher-button>
        </cv-content-switcher>
        <section style="margin: 10px 0;">
          <div class="content-1">
            <cv-search :placeholder="'Найти друзей'" @input="" @keyup.enter="findFriend"
                       v-model="newFriend" class="search"></cv-search>
            <FriendField v-for="friend in friends" :friend="friend" :delete-friend="deleteMyFriend"/>
          </div>
          <div class="content-2">
            <cv-search :placeholder="'Найти сервер'" @input="" class="search"></cv-search>
            <ServerField v-for="server in servers" :server="server" :getServerRooms="getCurServerRooms"/>
            <!--            <cv-button v-for="server in servers" @click="getCurServerRooms(server.id)" class="sidebar-item" kind="secondary" default="Primary">{{ server.name }}</cv-button>-->
            <cv-button @click="showServerModal" class="sidebar-item primary" kind="primary" default="Primary">Создать
              сервер
            </cv-button>
          </div>
        </section>
      </div>
      <div class="content">
        <div class="chat-sidebar">
          <div class="content-1">
            <RoomField v-for="room in rooms" :id="room.id" :name="room.name" :connect="connect"
                       :show-settings="showRoomSettings"/>
            <cv-button @click="showRoomModal" class="sidebar-item primary" kind="primary" default="Primary">Создать
              комнату
            </cv-button>
          </div>
          <div class="content-2">
            <ServerRoomField v-for="room in serverRooms" :id="room.id" :name="room.name" :connect="connect"/>
            <cv-button v-if="isOwner" @click="showServerRoomModal" class="sidebar-item primary" kind="primary">Создать
              канал
            </cv-button>
          </div>
        </div>
        <div class="chat">
          <div class="chat__messages">
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
}

.sidebar {
  width: 300px;
  background-color: #202225;
}

.content {
  display: flex;
  flex: 1;
}

.chat-sidebar {
  width: 300px;
  background-color: #292b2f;
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
}

.primary {
  border-radius: 3px;
  background-color: #7289da;
  margin: 10px;
  width: calc(100% - 20px);
}
</style>