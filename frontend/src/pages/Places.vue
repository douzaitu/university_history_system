<template>
  <div class="page">
    <div class="toolbar">
      <router-link to="/" class="back">← 返回首页</router-link>
    </div>
    <HeroBanner
      image="/HomePage/place.jpg"
      title="数字记忆 · 地点库"
      :height="320"
      description="地点库，主要收录与重庆大学相关的地理位置、建筑、地标等信息，它提供每个地点的图片、影像，以及与该地点相关联的人物、机构，以及相关事件，以帮助用户更好地了解和探索重庆大学的魅力。"
    />

    <div class="searchbar">
      <input
        v-model="query"
        class="search-input"
        placeholder="搜索地点、类别…"
        @keyup.enter="handleSearch"
      />
      <button v-if="query" @click="clearSearch" class="clear-btn">×</button>
      <button @click="handleSearch" class="search-btn">搜索</button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>正在加载数据...</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="!hasData" class="empty-state">
      <p>暂无地点数据</p>
      <button @click="fetchPlacesData" class="retry-btn">重新加载</button>
    </div>

    <!-- 数据展示 -->
    <div v-else>
      <div class="filter-options">
        <label class="filter-label">排序方式:</label>
        <select v-model="sortBy" class="sort-select">
          <option value="name">按名称</option>
          <option value="readCount">按阅读量</option>
        </select>

        <label class="filter-label">显示:</label>
        <select v-model="categoryFilter" class="category-select">
          <option value="">全部</option>
          <option
            v-for="category in uniqueCategories"
            :key="category"
            :value="category"
          >
            {{ category }}
          </option>
        </select>

        <span class="data-count"
          >共 {{ filteredAndSortedPlaces.length }} 条数据</span
        >
      </div>

      <div class="grid">
        <LibraryCard
          v-for="item in filteredAndSortedPlaces"
          :key="item.id"
          :title="item.name"
          :subtitle="item.category"
          :image="item.photo"
          :count="item.readCount"
          :to="`/places/${item.id}`"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import LibraryCard from "../components/LibraryCard.vue";
import HeroBanner from "../components/HeroBanner.vue";
// 添加API导入
import { getEntitiesByType, searchEntities } from "../api/knowledgeGraph";
import { ref, computed, onMounted } from "vue";

const query = ref("");
const sortBy = ref("name");
const categoryFilter = ref("");
const loading = ref(false);
// 改为从API获取数据
const placesData = ref([]);

// 在组件挂载时加载数据
onMounted(async () => {
  await fetchPlacesData();
});

// 获取地点数据的方法
const fetchPlacesData = async () => {
  try {
    loading.value = true;
    // 调用后端API获取地点类型实体
    const response = await getEntitiesByType("location");
    console.log("地点API返回数据:", response);

    // 将后端数据格式转换为前端需要的格式
    placesData.value = response.map((entity) => ({
      id: entity.id,
      name: entity.name,
      category: entity.entity_type,
      desc: entity.description,
      photo: "/Places/default.jpg", // 默认图片，后续可以从实体属性中获取
      readCount: 0, // 阅读量，后续可以从实体属性中获取
      lastUpdated: new Date().toISOString(),
      dataVersion: "1.0",
    }));

    console.log("转换后地点数据:", placesData.value);
  } catch (error) {
    console.error("加载地点数据失败:", error);
    // 可以添加用户友好的错误提示
  } finally {
    loading.value = false;
  }
};

// 搜索功能 - 修改为调用API
const handleSearch = async () => {
  const searchTerm = query.value.trim();

  if (!searchTerm) {
    await fetchPlacesData(); // 如果搜索为空，重新加载所有数据
    return;
  }

  try {
    loading.value = true;
    console.log("开始搜索地点:", searchTerm);

    // 使用搜索API
    const response = await searchEntities(searchTerm);
    console.log("地点搜索API返回:", response);

    if (response && response.length > 0) {
      // 转换数据格式，并过滤只保留地点类型
      placesData.value = response
        .filter((entity) => entity.entity_type === "location")
        .map((entity) => ({
          id: entity.id,
          name: entity.name,
          category: entity.entity_type,
          desc: entity.description,
          photo: "/Places/default.jpg",
          readCount: 0,
          lastUpdated: new Date().toISOString(),
        }));
      console.log("地点搜索成功，找到数据:", placesData.value.length, "条");
    } else {
      // 如果没有搜索结果，显示提示但不清空数据
      console.log("搜索无结果，保持原数据");
      // 可以在这里添加用户提示
    }
  } catch (error) {
    console.error("地点搜索失败:", error);
    // 搜索失败时也保持原数据不变
  } finally {
    loading.value = false;
  }
};

// 清空搜索
const clearSearch = () => {
  query.value = "";
  fetchPlacesData(); // 清空时重新加载所有数据
};

// 计算属性：是否有数据
const hasData = computed(() => placesData.value && placesData.value.length > 0);

// 计算属性：唯一的类别列表
const uniqueCategories = computed(() => {
  if (!placesData.value) return [];
  const categories = new Set(
    placesData.value.map((p) => p.category).filter(Boolean)
  );
  return Array.from(categories).sort();
});

// 计算属性：过滤和排序后的地点列表
const filteredAndSortedPlaces = computed(() => {
  let result = placesData.value;

  // 类别过滤
  if (categoryFilter.value) {
    result = result.filter((p) => p.category === categoryFilter.value);
  }

  // 关键词搜索（本地过滤，因为已经调用了搜索API）
  const q = query.value.trim().toLowerCase();
  if (q) {
    result = result.filter((place) => {
      const searchFields = [place.name, place.category, place.desc]
        .filter(Boolean)
        .map((v) => String(v).toLowerCase());

      return searchFields.some((field) => field.includes(q));
    });
  }

  // 排序
  if (sortBy.value === "name") {
    result = [...result].sort((a, b) => a.name.localeCompare(b.name));
  } else if (sortBy.value === "readCount") {
    result = [...result].sort(
      (a, b) => (b.readCount || 0) - (a.readCount || 0)
    );
  }

  return result;
});
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: linear-gradient(#2c2f30, #1e2122);
  padding: 20px;
  box-sizing: border-box;
  color: #fff;
}
.toolbar {
  display: flex;
  align-items: center;
  gap: 20px;
}
.back {
  color: #cfe9ff;
  text-decoration: none;
  font-size: 14px;
}
.title {
  margin: 0;
  font-size: 22px;
}
.desc {
  margin: 12px 0 20px;
  color: #cbd3d6;
}

.searchbar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin: 10px 0 16px;
  position: relative;
  gap: 8px;
}

.search-input {
  width: 260px;
  max-width: 50vw;
  padding: 8px 12px;
  padding-right: 32px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(0, 0, 0, 0.35);
  color: #fff;
  outline: none;
}
.search-input:focus {
  border-color: #4a9eff;
}
.search-input::placeholder {
  color: #cbd3d6;
}

.clear-btn {
  position: absolute;
  right: 70px;
  background: none;
  border: none;
  color: #cbd3d6;
  font-size: 18px;
  cursor: pointer;
  padding: 4px 8px;
}
.clear-btn:hover {
  color: #fff;
}

.search-btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(74, 158, 255, 0.8);
  color: #fff;
  cursor: pointer;
}
.search-btn:hover {
  background: rgba(74, 158, 255, 1);
}

.filter-options {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.filter-label {
  color: #cbd3d6;
  font-size: 14px;
}
.sort-select,
.category-select {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(0, 0, 0, 0.35);
  color: #fff;
  outline: none;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
  margin-top: 8px;
}

.loading {
  text-align: center;
  padding: 60px 20px;
  color: #cbd3d6;
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

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #cbd3d6;
  font-size: 16px;
}

.retry-btn {
  margin-top: 16px;
  padding: 8px 16px;
  border-radius: 6px;
  border: 1px solid #4a9eff;
  background: transparent;
  color: #4a9eff;
  cursor: pointer;
}

.data-count {
  margin-left: auto;
  color: #cbd3d6;
  font-size: 14px;
}
</style>
