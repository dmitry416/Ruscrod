<script setup lang="ts">
import {onMounted, ref} from "vue";
import apiClient from '@/axios';
import {getFriends} from "../../api/user.ts";
import {getRoomMembers, getRoomMessages, getRooms} from "../../api/room.ts";

const CHUNK = 500;

let audioContext: AudioContext | null = null;
let mediaStream: MediaStream | null = null;
let mediaRecorder: MediaRecorder | null = null;
let socket: WebSocket | null = null;

let token: string | null = null;
const userData: object = ref({
  default_avatar_id: '0/0-0',
  login: '',
});

const isConnected = ref(false);
const textMessage = ref("");

const cur_room_id = ref(1);

const messages = ['text1', 'text2', 'text3', 'jopa']
let newMessage: ''
const friends = ['Jack', 'Nigga', 'Pdior', "psdfsdf"]
const servers = ['Anal rooms', 'Small penis group']
const rooms = ['room1', 'room2', 'room3']

const selectedIndex = ref(-1);

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

async function connect(): Promise<void> {
  isConnected.value = true;
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
}

async function sendTextMessage(): Promise<void> {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({
      type: "text_message",
      data: textMessage.value,
      username: userData.value.login
    }));
    console.log('Текстовое сообщение отправлено:', textMessage.value);
  } else {
    console.error('WebSocket не подключен или не готов для отправки сообщений.');
  }
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
  await apiClient.post('auth', {login: login, image_url: image_url}).then(response => {
    console.log(response.data);
    localStorage.setItem("authToken", response.data.token);
  });
}

onMounted(async () => {
  window.history.replaceState({}, document.title, window.location.pathname);
  await getUserInfo().then(async (data) => {
    userData.value = data;
    await authDRF(data?.login, data?.default_avatar_id);
    console.log(userData.value);
    // дальше идут запросы для теста, ну и как пример вам
    await getFriends().then((request) => {
      console.log(request);
    })
    await getRooms().then((request) => {
      console.log(request);
    })
    await getRoomMessages(1, 1).then((request) => {
      console.log(request);
    })
  });
});
</script>
<!--  <div class="user-info">-->
<!--    <img :src="`https://avatars.yandex.net/get-yapic/${userData.default_avatar_id}/islands-retina-middle`"-->
<!--         alt="User Image" class="user-avatar">-->
<!--    <div class="user-name">{{ userData.login }}</div>-->
<!--  </div>-->
<!--  <div class="container">-->
<!--    <h1>Подключение по IP</h1>-->
<!--    <button v-if="!isConnected" @click="connect">Подключиться</button>-->
<!--    <button v-else @click="disconnect" style="background-color: #df3915">Отключиться</button>-->
<!--  </div>-->
<!--  <div v-if="isConnected" class="message-form">-->
<!--    <textarea placeholder="Введите ваше сообщение" v-model="textMessage"></textarea>-->
<!--    <button type="button" @click="sendTextMessage">Отправить</button>-->
<!--  </div>-->
<template>
  <div class="app">
    <header class="header">
      <div class="header__left">Ruscord</div>
      <div class="header__right">
        <span class="header__username">Имя пользователя</span>
        <img src="https://via.placeholder.com/40" alt="Avatar" class="header__avatar" />
      </div>
    </header>
    <div class="main">
      <div class="sidebar">
        <cv-content-switcher aria-label='Choose content'  @selected="onSelected">
          <cv-content-switcher-button content-selector=".content-1" :selected="selectedIndex === 0">Друзья</cv-content-switcher-button>
          <cv-content-switcher-button content-selector=".content-2" :selected="selectedIndex === 1">Сервера</cv-content-switcher-button>
        </cv-content-switcher>
        <section style="margin: 10px 0;">
          <div class="content-1">
            <cv-search :placeholder="'Найти друзей'" @input="onInput"></cv-search>
            <cv-button v-for="friend in friends" @click="onClick" class="sidebar-item" kind="secondary" default="Primary">{{friend}}</cv-button>
          </div>
          <div class="content-2">
            <cv-search :placeholder="'Найти сервер'" @input="onInput"></cv-search>
            <cv-button v-for="server in servers" @click="onClick" class="sidebar-item" kind="secondary" default="Primary">{{server}}</cv-button>
          </div>
        </section>
      </div>
      <div class="content">
        <div class="chat-sidebar">
          <div class="content-1">
            <cv-button v-for="room in rooms" @click="onClick" class="sidebar-item" kind="secondary" default="Primary">{{room}}</cv-button>
            <cv-button @click="onClick" class="sidebar-item" kind="primary" default="Primary">Создать комнату</cv-button>
          </div>
        </div>
        <div class="chat">
          <div class="chat__messages">
            <div v-for="message in messages" class="chat__message">
              <strong>{{ "username" }}:</strong> {{ message }}
            </div>
          </div>
          <div class="chat__input">
            <input
                v-model="newMessage"
                @keyup.enter="sendMessage"
                type="text"
                placeholder="Введите сообщение..."
                class="chat__input-field"
            />
            <button @click="sendMessage" class="chat__send-button">Отправить</button>
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
</style>