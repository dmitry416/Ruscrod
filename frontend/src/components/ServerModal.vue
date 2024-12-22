<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  data() {
    return {
      isVisible: false,
      serverName: "",
      imageFile: null as File | null,
    };
  },
  methods: {
    showModal(): void {
      this.isVisible = true;
      this.serverName = "";
      this.imageFile = null;
    },
    handleImageChange(event: Event): void {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        this.imageFile = target.files[0];
      }
    },
    createServer(): void {
      this.$props.onCreate(this.serverName, this.imageFile);
      this.isVisible = false;
    },
  },
  props: {
    onCreate: {
      type: Function,
      required: true,
    },
  }
});
</script>

<template>
  <cv-modal
    :visible="isVisible"
    size="sm"
    :autoHideOff="true"
    @modal-hide-request="isVisible = false"
    @primary-click="createServer"
  >
    <template v-slot:title>Создать сервер</template>
    <template v-slot:content>
      <cv-text-input
        label="Название сервера"
        placeholder="Введите название"
        v-model="serverName"
        @keyup.enter="createServer"
      />
      <cv-file-uploader
        label="Загрузить изображение"
        @change="handleImageChange"
      />
    </template>
    <template v-slot:primary-button>Создать</template>
  </cv-modal>
</template>

<style scoped>

</style>