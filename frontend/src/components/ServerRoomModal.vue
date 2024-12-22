<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      isVisible: false,
      value: "",
    };
  },
  methods: {
    showModal(): void {
      this.isVisible = true;
      this.value = "";
    },
  },
  props: {
    onCreate: {
      type: Function,
      required: true,
    },
  },
});
</script>

<template>
  <cv-modal
    :visible="isVisible"
    size="sm"
    :autoHideOff="true"
    @modal-hide-request="isVisible = false"
    @primary-click="onCreate(value); isVisible = false"
  >
    <template v-slot:title>Создать канал</template>
    <template v-slot:content>
      <cv-text-input
        label="Введите название канала"
        placeholder="Новый канал"
        v-model="value"
        @keyup.enter="onCreate(value); isVisible = false"
      />
    </template>
    <template v-slot:primary-button>Создать</template>
  </cv-modal>
</template>

<style scoped>
</style>