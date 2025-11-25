<template>
  <div class="detail-page">
    <div class="topbar">
      <router-link to="/organizations" class="back">← 返回机构库</router-link>
      <div class="site-title">
        数字记忆 · 知识详情 <span class="sub">dm.cdut.edu.cn</span>
      </div>
      <div class="actions">
        <button class="icon">🔍</button>
        <button class="icon">🏢</button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="organization" class="content">
      <h1 class="name">{{ organization.name }}</h1>
      <div class="meta-row">
        <span>{{ organization.readCount }} 阅读</span>
        <span>｜ 收藏</span>
      </div>

      <div class="body">
        <div class="left">
          <div class="field">
            <span class="label">名称</span
            ><span class="value">{{ organization.name }}</span>
          </div>
          <div class="field">
            <span class="label">类别</span
            ><span class="value">{{ organization.category }}</span>
          </div>
          <div class="bio">
            <div class="label">简介</div>
            <p class="text">{{ organization.desc }}</p>
          </div>
        </div>
        <div class="right">
          <div class="photo">
            <img :src="organization.photo" alt="photo" />
          </div>
        </div>
      </div>

      <div class="footer">
        <button class="pager">‹</button>
        <div class="progress"><div class="bar"></div></div>
        <button class="pager">›</button>
      </div>
    </div>

    <div v-else class="notfound">
      未找到机构信息。
      <router-link to="/organizations" class="back">返回机构库</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { getEntityDetail } from "../api/entityDetail";

const route = useRoute();
const organization = ref(null);
const loading = ref(false);

// 获取机构详情数据
const fetchOrganizationDetail = async (id) => {
  try {
    loading.value = true;
    console.log("加载机构详情，ID:", id);

    const response = await getEntityDetail(id);
    console.log("机构详情API返回:", response);

    if (response) {
      organization.value = {
        id: response.id,
        name: response.name,
        category: response.entity_type,
        desc: response.description,
        photo: "/Organizations/default.jpg",
        readCount: 0,
      };
    }
  } catch (error) {
    console.error("加载机构详情失败:", error);
    organization.value = null;
  } finally {
    loading.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  if (route.params.id) {
    fetchOrganizationDetail(route.params.id);
  }
});

// 监听路由变化
watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      fetchOrganizationDetail(newId);
    }
  }
);
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

.loading {
  text-align: center;
  padding: 60px 20px;
  color: #9a9a9a;
}

.loading-spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #4a9eff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
