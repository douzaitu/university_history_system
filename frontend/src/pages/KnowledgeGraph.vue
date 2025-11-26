<template>
  <div class="knowledge-graph-page">
    <!-- 顶部导航 -->
    <div class="topbar">
      <router-link to="/people" class="back">← 返回人物库</router-link>
      <div class="site-title">
        数字记忆 · 知识图谱 <span class="sub">dm.cdut.edu.cn</span>
      </div>
    </div>

    <!-- 搜索区域 -->
    <div class="search-section">
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="输入教师姓名搜索知识图谱..."
          class="search-input"
          @input="handleSearchInput"
          @keyup.enter="searchTeacher"
        />
        <button @click="searchTeacher" class="search-btn">搜索</button>

        <!-- 搜索结果下拉 -->
        <div v-if="searchResults.length > 0" class="search-results">
          <div
            v-for="teacher in searchResults"
            :key="teacher"
            class="result-item"
            @click="selectTeacher(teacher)"
          >
            {{ teacher }}
          </div>
        </div>
      </div>
    </div>

    <!-- 当前查询的教师 -->
    <div v-if="currentTeacher" class="current-teacher">
      <h3>正在查看: {{ currentTeacher }}</h3>
    </div>

    <!-- 图谱容器 -->
    <div class="graph-container">
      <div
        ref="graph"
        class="graph"
        :style="{
          height: graphHeight + 'px',
          width: '100%',
          minHeight: '400px',
        }"
      ></div>

      <!-- 加载状态 -->
      <div v-if="loading" class="graph-loading">
        <div class="loading-spinner"></div>
        <p>正在加载知识图谱...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!hasData && currentTeacher" class="graph-empty">
        <p>未找到 {{ currentTeacher }} 的相关知识图谱数据</p>
      </div>

      <!-- 初始状态 -->
      <div v-else-if="!currentTeacher" class="graph-initial">
        <p>请输入教师姓名搜索知识图谱</p>
      </div>
    </div>

    <!-- 图例 -->
    <div class="legend">
      <div class="legend-item">
        <div class="legend-color teacher"></div>
        <span>教师</span>
      </div>
      <div class="legend-item">
        <div class="legend-color entity"></div>
        <span>相关实体</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";

// 动态导入echarts
let echarts = null;

const router = useRouter();

// 状态管理
const searchQuery = ref("");
const searchResults = ref([]);
const currentTeacher = ref("");
const loading = ref(false);
const graph = ref(null);
const graphHeight = ref(600);
const chart = ref(null);
const errorMessage = ref("");

// 图谱数据
const graphData = ref({
  nodes: [],
  edges: [],
});

// 计算属性
const hasData = ref(false);

// 搜索教师
const searchTeacher = async () => {
  const teacherName = searchQuery.value.trim();
  if (!teacherName) return;

  try {
    loading.value = true;
    await loadTeacherGraph(teacherName);
    searchResults.value = [];
  } catch (error) {
    console.error("搜索失败:", error);
    hasData.value = false;
  } finally {
    loading.value = false;
  }
};

// 处理搜索输入
const handleSearchInput = async () => {
  const query = searchQuery.value.trim();

  if (!query) {
    searchResults.value = [];
    return;
  }

  try {
    console.log("开始搜索:", query);

    const response = await fetch(
      `http://localhost:8000/api/kg/search/?q=${encodeURIComponent(query)}`
    );

    console.log("搜索响应状态:", response.status);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("搜索返回数据:", data);

    // 确保teachers数组存在
    searchResults.value = data.teachers || [];
    console.log("处理后结果:", searchResults.value);
  } catch (error) {
    console.error("搜索建议失败:", error);
    searchResults.value = [];
  }
};

// 选择教师
const selectTeacher = (teacher) => {
  searchQuery.value = teacher;
  searchResults.value = [];
  searchTeacher();
};

// 加载教师图谱数据
const loadTeacherGraph = async (teacherName) => {
  try {
    loading.value = true;
    errorMessage.value = "";
    console.log("开始加载教师图谱:", teacherName);

    const response = await fetch(
      `http://localhost:8000/api/kg/teacher/${encodeURIComponent(teacherName)}/`
    );

    console.log("图谱API响应状态:", response.status);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("图谱API返回数据:", data);

    if (data.nodes && data.edges) {
      graphData.value = data;
      currentTeacher.value = teacherName;
      hasData.value = data.nodes.length > 0;
      console.log("图谱数据有效，节点数量:", data.nodes.length);

      // 直接渲染图谱
      renderGraph();
    } else {
      console.log("图谱数据无效");
      hasData.value = false;
      errorMessage.value = "未找到相关图谱数据";
    }
  } catch (error) {
    console.error("加载图谱数据失败:", error);
    hasData.value = false;
    errorMessage.value = "加载知识图谱失败: " + error.message;
  } finally {
    loading.value = false;
  }
};

// 渲染图谱
const renderGraph = async () => {
  if (!graph.value) {
    console.error("图谱容器未找到");
    return;
  }

  console.log("开始渲染图谱...");

  // 动态导入echarts
  if (!echarts) {
    try {
      echarts = await import("echarts");
      console.log("ECharts加载成功");
    } catch (error) {
      console.error("ECharts加载失败:", error);
      return;
    }
  }

  // 销毁旧图表
  if (chart.value) {
    chart.value.dispose();
    chart.value = null;
  }

  // 初始化图表
  try {
    chart.value = echarts.init(graph.value);
    console.log("ECharts初始化成功");
  } catch (error) {
    console.error("ECharts初始化失败:", error);
    return;
  }

  // 准备图表数据
  const nodes = graphData.value.nodes.map((node) => {
    const nodeSize = node.size || (node.type === "teacher" ? 25 : 15);

    return {
      id: node.id,
      name: node.label,
      symbolSize: nodeSize,
      itemStyle: {
        color: node.type === "teacher" ? "#5470c6" : "#91cc75",
      },
      label: {
        show: true,
        position: "right",
        formatter: "{b}",
      },
      category: node.type,
    };
  });

  const edges = graphData.value.edges.map((edge) => ({
    source: edge.source,
    target: edge.target,
    label: {
      show: true,
      formatter: edge.label || "关系",
    },
    lineStyle: {
      width: 2,
      color: "#aaa",
    },
  }));

  console.log("准备渲染的节点:", nodes);
  console.log("准备渲染的边:", edges);

  // 使用最简单的配置
  const option = {
    tooltip: {
      trigger: "item",
    },
    series: [
      {
        type: "graph",
        layout: "force",
        data: nodes,
        links: edges,
        roam: true,
        label: {
          show: true,
        },
        force: {
          repulsion: 100,
        },
      },
    ],
  };

  try {
    chart.value.setOption(option);
    console.log("图表渲染成功");

    // 确保图表正确调整大小
    setTimeout(() => {
      if (chart.value) {
        chart.value.resize();
      }
    }, 100);
  } catch (error) {
    console.error("图表渲染失败:", error);
  }

  // 响应窗口大小变化
  window.addEventListener("resize", handleResize);
};

// 处理窗口大小变化
const handleResize = () => {
  if (chart.value) {
    chart.value.resize();
  }
};

// 组件挂载
onMounted(() => {
  // 设置图谱高度
  graphHeight.value = window.innerHeight - 200;
});

// 组件卸载
onUnmounted(() => {
  if (chart.value) {
    chart.value.dispose();
  }
  window.removeEventListener("resize", handleResize);
});
</script>

<style scoped>
.knowledge-graph-page {
  min-height: 100vh;
  background: #f7f4f3;
}

.topbar {
  height: 56px;
  background: #2b2b2b;
  color: #eaeaea;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
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

.search-section {
  padding: 20px;
  background: white;
  border-bottom: 1px solid #e0e0e0;
}

.search-container {
  position: relative;
  max-width: 400px;
  margin: 0 auto;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
  font-size: 16px;
  box-sizing: border-box;
}

.search-input:focus {
  border-color: #4a9eff;
}

.search-btn {
  position: absolute;
  right: 4px;
  top: 4px;
  padding: 8px 16px;
  background: #4a9eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-btn:hover {
  background: #2a7fff;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 4px 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.result-item {
  padding: 10px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  color: #333;
}

.result-item:hover {
  background: #f5f5f5;
}

.result-item:last-child {
  border-bottom: none;
}

.current-teacher {
  padding: 10px 20px;
  text-align: center;
  background: white;
  margin: 0 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.graph-container {
  position: relative;
  margin: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  min-height: 600px;
  width: 100%;
}

.graph {
  width: 100%;
  height: 600px;
  min-height: 600px;
}

.graph-loading,
.graph-empty,
.graph-initial {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #666;
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

.legend {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: white;
  padding: 10px 16px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.legend-color.teacher {
  background: #5470c6;
}

.legend-color.entity {
  background: #91cc75;
}
</style>
