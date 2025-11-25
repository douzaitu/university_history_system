<template>
  <div class="lib-card" @click="handleClick">
    <div class="thumb">
      <div v-if="loading" class="loading-placeholder">
        <div class="skeleton"></div>
      </div>
      <img 
        v-if="imageUrl" 
        :src="imageUrl" 
        :alt="title"
        @load="onImageLoad"
        @error="onImageError"
        class="card-image"
        loading="lazy"
      />
      <div v-else class="no-image">
        <span class="no-image-text">{{ getInitials(title) }}</span>
      </div>
    </div>
    <div class="info">
      <h3 class="title">{{ title || '未知姓名' }}</h3>
      <p class="subtitle" v-if="subtitle">{{ subtitle }}</p>
      <div class="meta">
        <span class="count">{{ formattedCount }}</span>
        <span class="view">查看 →</span>
      </div>
    </div>
    <div v-if="isFavorite" class="favorite-indicator">❤️</div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const props = defineProps({
  title: String,
  subtitle: String,
  image: String,
  count: [String, Number],
  to: String,
  favorite: Boolean
})

const loading = ref(true)
const imageUrl = ref(props.image)

// 计算是否为收藏
const isFavorite = computed(() => {
  if (props.favorite !== undefined) return props.favorite
  
  // 从localStorage获取收藏状态
  const favorites = JSON.parse(localStorage.getItem('favoritePeople') || '[]')
  // 尝试从to属性中提取ID
  if (props.to && props.to.startsWith('/people/')) {
    const id = props.to.split('/').pop()
    return favorites.includes(id)
  }
  return false
})

// 格式化计数
const formattedCount = computed(() => {
  const count = Number(props.count || 0)
  if (count >= 1000) {
    return (count / 1000).toFixed(1) + 'k'
  }
  return Intl.NumberFormat().format(count)
})

// 获取姓名首字母作为默认显示
const getInitials = (name) => {
  if (!name || typeof name !== 'string') return '?'
  
  // 对于中文名，返回姓
  if (/^[\u4e00-\u9fa5]/.test(name)) {
    return name.charAt(0)
  }
  
  // 对于英文名，返回首字母
  return name.charAt(0).toUpperCase()
}

// 处理图片加载
const onImageLoad = () => {
  loading.value = false
}

// 处理图片错误
const onImageError = () => {
  loading.value = false
  imageUrl.value = null // 使用文字占位符
}

// 处理点击事件
const handleClick = (event) => {
  // 阻止事件冒泡
  event.stopPropagation()
  
  if (props.to) {
    router.push(props.to)
  }
}
</script>

<style scoped>
.lib-card{
  width: 100%;
  min-width: 220px;
  background:#ffffff;
  border-radius:12px;
  overflow:hidden;
  box-shadow:0 4px 12px rgba(0, 0, 0, 0.1);
  cursor:pointer;
  transition:all 0.3s ease;
  position:relative;
  display:flex;
  flex-direction:column;
  height:100%;
}

.lib-card:hover{
  transform:translateY(-6px);
  box-shadow:0 12px 24px rgba(0, 0, 0, 0.15);
}

.thumb{
  height:180px;
  background:#f0f0f0;
  display:flex;
  align-items:center;
  justify-content:center;
  position:relative;
  overflow:hidden;
}

.loading-placeholder{
  width:100%;
  height:100%;
  display:flex;
  align-items:center;
  justify-content:center;
}

.skeleton{
  width:80%;
  height:80%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius:4px;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.card-image{
  width:100%;
  height:100%;
  object-fit:cover;
  display:block;
  transition:transform 0.3s ease;
}

.lib-card:hover .card-image{
  transform:scale(1.05);
}

.no-image{
  width:100%;
  height:100%;
  display:flex;
  align-items:center;
  justify-content:center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color:white;
}

.no-image-text{
  font-size:48px;
  font-weight:bold;
  text-shadow:2px 2px 4px rgba(0,0,0,0.2);
}

.info{
  padding:16px;
  flex-grow:1;
  display:flex;
  flex-direction:column;
}

.title{
  margin:0;
  font-size:18px;
  color:#333;
  font-weight:600;
  line-height:1.3;
  display:-webkit-box;
  -webkit-line-clamp:2;
  -webkit-box-orient:vertical;
  overflow:hidden;
  text-overflow:ellipsis;
}

.subtitle{
  margin:8px 0 12px;
  font-size:12px;
  color:#666;
  background:#f5f5f5;
  padding:4px 8px;
  border-radius:12px;
  align-self:flex-start;
}

.meta{
  margin-top:auto;
  display:flex;
  justify-content:space-between;
  align-items:center;
}

.count{
  background:#f0f4f8;
  color:#666;
  border-radius:12px;
  padding:4px 8px;
  font-size:12px;
  font-weight:500;
}

.view{
  font-size:12px;
  color:#4a9eff;
  font-weight:500;
  transition:color 0.2s ease;
}

.lib-card:hover .view{
  color:#1677ff;
}

.favorite-indicator{
  position:absolute;
  top:8px;
  right:8px;
  font-size:16px;
  text-shadow:0 1px 2px rgba(0,0,0,0.3);
  z-index:10;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .lib-card{
    min-width:unset;
  }
  
  .thumb{
    height:160px;
  }
  
  .title{
    font-size:16px;
  }
}
</style>