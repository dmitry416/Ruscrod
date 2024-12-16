<script setup lang="ts">
import {VOICECHAT_URL} from "@/config.ts";
import {onMounted, ref} from "vue";

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


async function initAudio(): Promise<void> {
  audioContext = new AudioContext();
  mediaStream = await navigator.mediaDevices.getUserMedia({audio: true});
  mediaRecorder = new MediaRecorder(mediaStream);

  mediaRecorder.ondataavailable = async (event: BlobEvent) => {
    if (event.data.size > 0) {
      await event.data.arrayBuffer().then(
          (buffer) => {
            socket?.send(buffer);
            mediaRecorder?.stop();
            mediaRecorder?.start(CHUNK);
          }
      );
    }
  };

  socket = new WebSocket(`ws://127.0.0.1:8000/ws/${VOICECHAT_URL}`);
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
    socket.send(textMessage.value);
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

onMounted(async () => {
  window.history.replaceState({}, document.title, window.location.pathname);
  await getUserInfo().then((data) => {
    userData.value = data;
    console.log(userData.value);
  });
});
</script>

<template>
  <div class="user-info">
    <img :src="`https://avatars.yandex.net/get-yapic/${userData.default_avatar_id}/islands-retina-middle`"
         alt="User Image" class="user-avatar">
    <div class="user-name">{{ userData.login }}</div>
  </div>
  <div class="container">
    <h1>Подключение по IP</h1>
    <button v-if="!isConnected" @click="connect">Подключиться</button>
    <button v-else @click="disconnect" style="background-color: #df3915">Отключиться</button>
  </div>
  <div v-if="isConnected" class="message-form">
    <textarea placeholder="Введите ваше сообщение" v-model="textMessage"></textarea>
    <button type="button" @click="sendTextMessage">Отправить</button>
  </div>
</template>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}

.container {
  background: #fff;
  padding: 20px 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #218838;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  max-width: 300px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.message-form {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.message-form textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;
}

.message-form button {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.message-form button:hover {
  background-color: #218838;
}
</style>