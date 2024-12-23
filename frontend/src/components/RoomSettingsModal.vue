<script lang="ts">
import { defineComponent } from 'vue';
import FriendField from "@/components/FriendField.vue";
import ServerField from "@/components/ServerField.vue";

export default defineComponent({
  components: {ServerField, FriendField},
  data() {
    return {
      isVisible: false,
      selectedIndex: 0,
      id: 0,
      newRoomName: "",
      newFriendName: "",
      curName: "",
    };
  },
  methods: {
    showModal(id: number, curName: string): void {
      this.isVisible = true;
      this.id = id;
      this.newRoomName = curName;
      this.curName = curName;
    },
    saveChanges(): void {
      if (this.newFriendName) {
        this.onAddFriend(this.id, this.newFriendName);
      }
      if (this.newRoomName !== this.curName) {
        this.onChangeName(this.id, this.newRoomName);
      }
    }
  },
  props: {
    onChangeName: {
      type: Function,
      required: true,
    },
    onAddFriend: {
      type: Function,
      required: true,
    },
    onLeave: {
      type: Function,
      required: true,
    },
  }
});
</script>

<template>
  <cv-modal :visible="isVisible"
            size="sm"
            :autoHideOff="true"
            @modal-hide-request="isVisible = false"
            @primary-click="saveChanges(); isVisible=false">
    <template v-slot:title>Редактировать комнату</template>
    <template v-slot:content>
      <cv-content-switcher aria-label='Choose content' @selected="" id="roomSettings">
        <cv-content-switcher-button owner-id="content-1" parent-switcher="roomSettings" :selected="selectedIndex === 0">Комната</cv-content-switcher-button>
        <cv-content-switcher-button owner-id="content-2" parent-switcher="roomSettings" :selected="selectedIndex === 1">Пользователи</cv-content-switcher-button>
      </cv-content-switcher>
      <section style="margin: 10px 0;">
        <cv-content-switcher-content parent-switcher="roomSettings" owner-id="content-1">
          <cv-text-input label="Изменить название комнаты" placeholder="Новое название комнаты" v-model="newRoomName"/>
          <cv-button @click="onLeave(id); isVisible=false;" kind="danger" class="delete">Выйти из комнаты</cv-button>
        </cv-content-switcher-content>
        <cv-content-switcher-content parent-switcher="roomSettings" owner-id="content-2">
          <cv-text-input label="Добавить пользователя" placeholder="Имя друга" v-model="newFriendName"/>
        </cv-content-switcher-content>
      </section>

    </template>
    <template v-slot:primary-button>Сохранить</template>
  </cv-modal>
</template>

<style scoped>
.delete {
  width: 100%;
  margin-top: 10px;
  background-color: #df3d3d;
  border-radius: 3px;
}
</style>