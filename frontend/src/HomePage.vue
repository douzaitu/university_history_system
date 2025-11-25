<template>
  <div class="home">
    <h1 class="site-title">校史馆数字记忆 · 首页</h1>

    <div class="card-row">
      <Card title="人物" desc="以知识图谱形式收录计算机与网络安全学院相关人物" count="101" to="/people" image="/HomePage/peopel.jpg" />
      <Card title="地点" desc="收录与计算机与网络安全学院相关的地理位置、建筑等" count="1" to="/places" image="/HomePage/place.jpg" />
      <Card title="学科" desc="学科库为用户提供了解计算机与网络安全学院学科的信息" count="1" to="/subjects" image="/HomePage/subject.gif" />
      <Card title="机构" desc="收录与计算机与网络安全学院相关的组织和机构资料" count="1" to="/organizations" image="/HomePage/机构.jpg" />
      <Card title="事件" desc="记录与计算机与网络安全学院相关的重要事件" count="1" to="/events" image="/HomePage/事件.jpg" />
    </div>
  </div>
</template>

<script setup>
import Card from './components/Card.vue'
</script>

<style scoped>
.home{
  min-height:100vh;
  padding:28px 20px;
  background: linear-gradient(#dde3e3, #7c8080);
  box-sizing:border-box;
}
.site-title{
  text-align:center;
  color:#fff;
  font-size:20px;
  margin:6px 0 18px;
  text-shadow:0 2px 6px rgba(0,0,0,0.4);
}
.card-row{
  display:flex;
  justify-content:center;
  gap:20px;
  padding:20px;
  flex-wrap:nowrap;
  overflow:auto;
  align-items:flex-start;
}
</style>