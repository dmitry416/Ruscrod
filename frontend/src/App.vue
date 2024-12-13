<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ref } from "vue";

const CHUNK = 500;

let audioContext: AudioContext | null = null;
let mediaStream: MediaStream | null = null;
let mediaRecorder: MediaRecorder | null = null;
let socket: WebSocket | null = null;

const isConnected = ref(false);


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

  socket = new WebSocket(`ws://127.0.0.1:8000/ws/audio`);
  socket.binaryType = 'arraybuffer';

  socket.onmessage = (event: MessageEvent) => {
    const arrayBuffer = event.data as ArrayBuffer;
    audioContext?.decodeAudioData(arrayBuffer, (buffer: AudioBuffer) => {
      const source = audioContext?.createBufferSource();
      if (source) {
        source.buffer = buffer;
        source.connect(audioContext?.destination as AudioNode);
        source.start();
      }
    });
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
</script>

<template>
  <div class="container">
    <h1>Подключение по IP</h1>
    <button v-if="!isConnected" @click="connect">Подключиться</button>
    <button v-else @click="disconnect" style="background-color: #df3915">Отключиться</button>
  </div>

  <RouterView/>
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
</style>
