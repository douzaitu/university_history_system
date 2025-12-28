<template>
  <div id="app">
    <RouterView />
    <!-- AI助手组件 -->
    <AIAssistant />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import AIAssistant from "./components/AIAssistant.vue";
</script>

<style>
body {
  margin: 0;
  font-family: "Microsoft YaHei", sans-serif;
  background-color: #f5f6f7;
}
</style>
