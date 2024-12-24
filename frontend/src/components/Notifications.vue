<script lang="ts">
import { defineComponent } from 'vue';

interface Notification {
  kind: string;
  title: string;
  caption: string;
}

export default defineComponent({
  data() {
    return {
      notifications: [] as Notification[],
    };
  },
  methods: {
    addNotification(caption:string, autoDestroy=true): void {
      if (caption.error) {
        this.notifications.push({ kind: "error", title: "Ошибка", caption: caption.error });
      }
      else if (caption.warning) {
        this.notifications.push({ kind: "warning", title: "Внимание", caption: caption.warning });
      }
      else {
        this.notifications.push({ kind: "success", title: "Успешно", caption: caption.success });
      }
      if (autoDestroy) {
        setTimeout(() => this.removeNotification(this.notifications.length - 1), 5000);
      }
    },
    removeNotification(index: number) {
      this.notifications.splice(index, 1);
    },
  },
});
</script>

<template>
  <div class="notification-zone">
    <cv-toast-notification
        v-for="(notification, index) in notifications"
        :key="index"
        :kind="notification.kind"
        :title="notification.title"
        :caption="notification.caption"
        @close="removeNotification(index)"
    ></cv-toast-notification>
  </div>
</template>

<style scoped>
.notification-zone {
  position: fixed;
  bottom: 20px;
  left: 20px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}
</style>