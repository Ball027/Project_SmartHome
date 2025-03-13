<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

export default {
  name: "App",
  setup() {
    const store = useStore();
    const isAuthenticated = computed(() => store.getters["auth/isAuthenticated"]);

    return { isAuthenticated };
  },
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}
</style>
