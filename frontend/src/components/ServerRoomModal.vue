<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  data() {
    return {
      isVisible: false,
      selectedIndex: 0,
      newServerName: "",
      newImageFile: null as File | null,
      newChannelName: ""
    };
  },
  emits: ['update-server', 'delete-server', 'create-channel'],
  methods: {
    showModal(): void {
      this.isVisible = true;
      this.newServerName = "";
      this.newImageFile = null;
      this.newChannelName = "";
      (this.$refs.fileUploader as any).clear();
    },
    handleImageChange(event: Event): void {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        const file = target.files[0];
        const allowedTypes = ['image/jpeg', 'image/png'];
        if (!allowedTypes.includes(file.type)) {
          this.newImageFile = null;
          return;
        }
        this.newImageFile = file;
      }
    },
    saveChanges(): void {
      const updateData = {
        name: this.newServerName,
        image: this.newImageFile
      };
      this.$emit('update-server', updateData);
      this.isVisible = false;
    },
    deleteServer(): void {
      this.$emit('delete-server');
      this.isVisible = false;
    },
    createChannel(): void {
      this.$emit('create-channel', this.newChannelName);
      this.newChannelName = "";
    }
  }
})
</script>

<template>
  <cv-modal :visible="isVisible"
            size="sm"
            :autoHideOff="true"
            @modal-hide-request="isVisible = false"
            @primary-click="saveChanges">
    <template v-slot:title>Управление сервером</template>
    <template v-slot:content>
      <cv-content-switcher aria-label='Choose content' @selected="selectedIndex = $event" id="serverSettings">
        <cv-content-switcher-button owner-id="content-1" parent-switcher="serverSettings"
                                    :selected="selectedIndex === 0">Сервер
        </cv-content-switcher-button>
        <cv-content-switcher-button owner-id="content-2" parent-switcher="serverSettings"
                                    :selected="selectedIndex === 1">Управление
        </cv-content-switcher-button>
        <cv-content-switcher-button owner-id="content-3" parent-switcher="serverSettings"
                                    :selected="selectedIndex === 2">Создать канал
        </cv-content-switcher-button>
      </cv-content-switcher>
      <section style="margin: 10px 0;">
        <cv-content-switcher-content parent-switcher="serverSettings" owner-id="content-1">
          <cv-text-input label="Изменить название сервера" placeholder="Новое название сервера"
                         v-model="newServerName"/>
          <cv-file-uploader
              ref="fileUploader"
              dropTargetLabel="Загрузить изображение сервера"
              accept=".jpg,.png"
              kind="button"
              :clearOnReselect="true"
              :multiple="false"
              @change="handleImageChange"
          />
        </cv-content-switcher-content>
        <cv-content-switcher-content parent-switcher="serverSettings" owner-id="content-2">
          <cv-button @click="deleteServer" kind="danger" class="delete">Удалить сервер</cv-button>
        </cv-content-switcher-content>
        <cv-content-switcher-content parent-switcher="serverSettings" owner-id="content-3">
          <cv-text-input
              label="Название канала"
              placeholder="Введите название канала"
              v-model="newChannelName"
              @keyup.enter="createChannel"
          />
          <cv-button @click="createChannel" kind="primary" class="create">Создать канал</cv-button>
        </cv-content-switcher-content>
      </section>
    </template>
    <template v-slot:primary-button v-if="selectedIndex === 'content-1' || selectedIndex === 0">Сохранить</template>
  </cv-modal>
</template>

<style scoped>
.delete {
  width: 100%;
  margin-top: 10px;
  background-color: #df3d3d;
  border-radius: 3px;
}

.create {
  width: 100%;
  margin-top: 10px;
  background-color: #7289da;
  border-radius: 3px;
}
</style>