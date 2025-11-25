<template>
  <div class="card" @click="handleClick">
    <div class="card-image" :style="imageStyle"></div>
    <div class="card-body">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-desc">{{ desc }}</p >
      <div class="card-meta">
        <span class="count">{{ formattedCount }}</span>
        <span class="view">查看 →</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const props = defineProps({
  title: String,
  desc: String,
  count: [String, Number],
  to: String,
  image: String
})
const emit = defineEmits(['open'])
const formattedCount = computed(()=> Intl.NumberFormat().format(Number(props.count || 0)))
const imageStyle = computed(() => ({
  backgroundImage: props.image
    ? `linear-gradient(180deg, rgba(0,0,0,0.06), rgba(0,0,0,0)), url(${props.image})`
    : 'linear-gradient(180deg, rgba(0,0,0,0.06), rgba(0,0,0,0))'
}))
function handleClick(){
  if (props.to) {
    router.push(props.to)
  } else {
    emit('open')
    console.log('打开：', props.title)
  }
}
</script>

<style scoped>
.card{
  width: 260px;
  min-width: 260px;
  height: 700px;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(to bottom, rgb(240, 243, 243), rgba(109, 218, 243, 0.756));
  box-shadow: 0 10px 30px rgba(12, 12, 12, 0.18);
  display:flex;
  flex-direction:column;
  cursor:pointer;
  transition: transform .22s ease, box-shadow .22s ease;
}
.card:hover{ transform: translateY(-8px); box-shadow: 0 18px 40px rgba(0,0,0,0.22); }

.card-image{
  height:310px;
  background-size:cover;
  background-position:center;
  /* 这里可以放占位色或图片 */
  background-color:#ebe8ec;
}

.card-body{
  padding:18px;
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  flex:1;
}
.card-title{
  font-size:28px;
  margin:0;
  color:#27414a;
}
.card-desc{
  margin:10px 0 0;
  font-size:13px;
  color:#4a5b5f;
  height:90px;
  overflow:hidden;
}
.card-meta{
  display:flex;
  justify-content:space-between;
  align-items:center;
}
.count{
  background:#e9eef0;
  padding:6px 10px;
  border-radius:8px;
  font-weight:600;
}
.view{ color:#2b6b86; font-size:13px; }
</style>