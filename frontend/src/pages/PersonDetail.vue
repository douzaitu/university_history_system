<template>
  <div class="detail-page">
    <div class="topbar">
      <router-link to="/people" class="back">← 返回人物库</router-link>
      <div class="site-title">
        数字记忆 · 人物详情 <span class="sub">dm.cdut.edu.cn</span>
      </div>
      <div class="actions">
        <button class="icon" @click="handleSearch">🔍</button>
        <button class="icon" @click="toggleFavorite">
          {{ isFavorite ? "❤️" : "🤍" }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="person" class="content">
      <div class="header-section">
        <h1 class="name">{{ person.name }}</h1>
        <div class="meta-row">
          <span class="read-count">{{ person.readCount }} 阅读</span>
          <span class="separator">｜</span>
          <span class="update-time">{{
            formatUpdateTime(person.lastUpdated)
          }}</span>
        </div>
      </div>

      <div class="body">
        <div class="left">
          <div class="info-card">
            <div class="field">
              <span class="label">姓名</span
              ><span class="value">{{ person.name }}</span>
            </div>
            <div class="field">
              <span class="label">职位/类别</span
              ><span class="value">{{ person.category }}</span>
            </div>
            <div class="field">
              <span class="label">数据版本</span
              ><span class="value">{{ person.dataVersion || "1.0" }}</span>
            </div>
          </div>

          <div class="bio-card">
            <div class="label">人物简介</div>
            <div class="text-content">
              <p
                v-for="(paragraph, idx) in formattedBio"
                :key="idx"
                class="paragraph"
              >
                {{ paragraph }}
              </p>
            </div>
          </div>

          <!-- 添加分享和操作按钮 -->
          <div class="action-buttons">
            <button class="btn" @click="sharePerson">分享</button>
            <button class="btn" @click="increaseReadCount">点赞</button>
          </div>
        </div>

        <div class="right">
          <div class="photo-container">
            <img
              :src="person.photo"
              :alt="`${person.name}的照片`"
              @error="handleImageError"
              class="person-photo"
            />
            <div v-if="showDefaultPhoto" class="default-photo-overlay">
              默认头像
            </div>
          </div>

          <!-- 可以添加相关人物推荐 -->
          <div v-if="relatedPeople.length > 0" class="related-people">
            <h3>相关人物</h3>
            <div class="related-list">
              <router-link
                v-for="related in relatedPeople"
                :key="related.id"
                :to="`/people/${related.id}`"
                class="related-item"
              >
                {{ related.name }}
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- 注释掉前后导航部分，因为目前没有实现这个功能 -->
      <!-- 
      <div class="navigation">
        <router-link
          v-if="previousPerson"
          :to="`/people/${previousPerson.id}`"
          class="nav-btn prev"
        >
          ‹ {{ previousPerson.name }}
        </router-link>
        <div class="nav-spacer" v-if="!previousPerson"></div>
        <router-link
          v-if="nextPerson"
          :to="`/people/${nextPerson.id}`"
          class="nav-btn next"
        >
          {{ nextPerson.name }} ›
        </router-link>
      </div>
      -->
    </div>

    <div v-else class="notfound">
      <div class="notfound-content">
        <h2>未找到人物信息</h2>
        <p>您访问的人物信息不存在或已被移除</p>
        <router-link to="/people" class="back-btn">返回人物库</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { getEntityDetail } from "../api/entityDetail";

const route = useRoute();

// 状态管理
const person = ref(null);
const loading = ref(false);
const isFavorite = ref(false);
const showDefaultPhoto = ref(false);

// 加载人物详情数据
const fetchPersonDetail = async (id) => {
  try {
    loading.value = true;
    console.log("加载人物详情，ID:", id);

    const response = await getEntityDetail(id);
    console.log("人物详情API返回:", response);

    if (response) {
      person.value = {
        id: response.id,
        name: response.name,
        category: response.entity_type,
        bio: response.description,
        // 修复这里：使用实际的photo_url，如果没有则使用默认图片
        photo: response.photo_url
          ? `http://localhost:8000/media/${response.photo_url}`
          : "/People/default.jpg",
        readCount: 0,
        lastUpdated: new Date().toISOString(),
        dataVersion: "1.0",
      };

      // 检查收藏状态
      checkFavoriteStatus();

      // 增加阅读计数
      increaseReadCount();
    }
  } catch (error) {
    console.error("加载人物详情失败:", error);
    person.value = null;
  } finally {
    loading.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  if (route.params.id) {
    fetchPersonDetail(route.params.id);
  }
});

// 监听路由变化
watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      fetchPersonDetail(newId);
    }
  }
);

// 格式化简介内容，按句号分段
const formattedBio = computed(() => {
  if (!person.value?.bio) return ["暂无简介"];

  // 将长文本按句号分段
  return person.value.bio
    .split(/[。.]/)
    .map((p) => p.trim())
    .filter((p) => p.length > 0)
    .map((p) => p + "。");
});

// 相关人物（暂时设为空，因为需要额外API支持）
const relatedPeople = computed(() => {
  return [];
});

// 图片加载错误处理
const handleImageError = (event) => {
  event.target.src = "/People/default.jpg";
  showDefaultPhoto.value = true;
};

// 格式化更新时间
const formatUpdateTime = (timestamp) => {
  if (!timestamp) return "未知";

  const date = new Date(timestamp);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(
    2,
    "0"
  )}-${String(date.getDate()).padStart(2, "0")}`;
};

// 切换收藏状态
const toggleFavorite = () => {
  isFavorite.value = !isFavorite.value;

  // 保存收藏状态到localStorage
  const favorites = JSON.parse(localStorage.getItem("favoritePeople") || "[]");
  if (isFavorite.value && person.value) {
    if (!favorites.includes(person.value.id)) {
      favorites.push(person.value.id);
    }
  } else if (person.value) {
    const index = favorites.indexOf(person.value.id);
    if (index > -1) {
      favorites.splice(index, 1);
    }
  }
  localStorage.setItem("favoritePeople", JSON.stringify(favorites));
};

// 检查收藏状态
const checkFavoriteStatus = () => {
  if (!person.value) return;

  const favorites = JSON.parse(localStorage.getItem("favoritePeople") || "[]");
  isFavorite.value = favorites.includes(person.value.id);
};

// 增加阅读计数
const increaseReadCount = () => {
  if (!person.value) return;

  // 简单的内存中增加计数
  person.value.readCount = (person.value.readCount || 0) + 1;

  // 如果需要持久化，可以保存到localStorage
  const readCounts = JSON.parse(
    localStorage.getItem("personReadCounts") || "{}"
  );
  readCounts[person.value.id] = (readCounts[person.value.id] || 0) + 1;
  localStorage.setItem("personReadCounts", JSON.stringify(readCounts));
};

// 分享功能（占位）
const sharePerson = () => {
  if (!person.value) return;

  const shareText = `查看${person.value.name}的详细信息 - 数字记忆系统`;
  const shareUrl = window.location.href;

  // 简单的复制到剪贴板
  navigator.clipboard
    .writeText(`${shareText}: ${shareUrl}`)
    .then(() => alert("分享链接已复制到剪贴板"))
    .catch((err) => console.error("复制失败:", err));
};

// 搜索功能（占位）
const handleSearch = () => {
  // 可以实现简单的搜索界面或跳转到搜索页面
  alert("搜索功能即将推出");
};
</script>

<style scoped>
.detail-page {
  min-height: 100vh;
  background: #f7f4f3;
  color: #2b2b2b;
}
.topbar {
  height: 56px;
  background: #2b2b2b;
  color: #eaeaea;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 14px;
  box-sizing: border-box;
}
.back {
  color: #cfe9ff;
  text-decoration: none;
}
.site-title {
  font-weight: 600;
}
.site-title .sub {
  font-weight: 400;
  font-size: 12px;
  color: #c5c5c5;
  margin-left: 6px;
}
.actions .icon {
  background: transparent;
  border: none;
  color: #eaeaea;
  font-size: 16px;
  margin-left: 10px;
  cursor: pointer;
}
.content {
  padding: 20px;
}
.name {
  font-size: 30px;
  margin: 10px 0 6px;
}
.meta-row {
  color: #9a9a9a;
  font-size: 12px;
}
.body {
  display: flex;
  gap: 30px;
  margin-top: 10px;
}
.left {
  flex: 1;
}
.field {
  display: flex;
  gap: 16px;
  padding: 10px 0;
  border-bottom: 1px dashed #ddd;
}
.label {
  width: 90px;
  color: #7c7c7c;
}
.value {
  color: #333;
}
.bio {
  margin-top: 18px;
}
.text {
  line-height: 1.75;
  text-align: justify;
}
.right {
  width: 300px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}
.photo {
  background: #fff;
  border: 1px solid #ddd;
  padding: 10px;
}
.photo img {
  width: 100%;
  height: auto;
  display: block;
}
.footer {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 60px;
  background: #1f1f1f;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}
.pager {
  background: #333;
  color: #fff;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 18px;
  cursor: pointer;
}
.progress {
  width: 260px;
  height: 6px;
  background: #444;
  border-radius: 10px;
  overflow: hidden;
}
.bar {
  width: 30%;
  height: 100%;
  background: #bbb;
}
.notfound {
  padding: 20px;
}
.photo-container {
  width: 300px;
  height: 300px;
  overflow: hidden;
  border-radius: 8px;
  border: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
}

.person-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
</style>
