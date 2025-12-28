<template>
  <div class="ai-assistant">
    <!-- 悬浮按钮 -->
    <button class="assistant-btn" @click="toggleChat">🤖</button>

    <!-- 聊天窗口 -->
    <div v-if="showChat" class="chat-window">
      <div class="chat-header">
        <h3>AI助手</h3>
        <button class="close-btn" @click="closeChat">×</button>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.role]"
        >
          {{ message.content }}
        </div>

        <div v-if="loading" class="message ai loading">正在思考中...</div>
      </div>

      <div class="chat-input">
        <input
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="有什么问题想问我的吗？"
          :disabled="loading"
        />
        <button @click="sendMessage" :disabled="loading || !userInput.trim()">
          发送
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from "vue";
import axios from "axios";

const showChat = ref(false);
const userInput = ref("");
const messages = ref([]);
const loading = ref(false);
const messagesContainer = ref(null);

// 预定义一些欢迎语
const welcomeMessages = [
  "你好！我是校史知识图谱的AI助手，我可以帮你查询学校相关的信息。",
  "你可以问我关于学校历史、人物、事件等各种问题。",
  "比如：'赵仕波老师的研究方向是什么？' 或 '计算机学院有哪些老师？'",
];

// 初始化消息
messages.value = welcomeMessages.map((msg) => ({
  role: "ai",
  content: msg,
}));

// 切换聊天窗口
const toggleChat = () => {
  showChat.value = !showChat.value;
  if (showChat.value) {
    scrollToBottom();
  }
};

// 关闭聊天窗口
const closeChat = () => {
  showChat.value = false;
};

// 发送消息
const sendMessage = async () => {
  const question = userInput.value.trim();
  if (!question || loading.value) return;

  // 添加用户消息
  messages.value.push({
    role: "user",
    content: question,
  });

  userInput.value = "";
  loading.value = true;

  // 滚动到底部
  scrollToBottom();

  try {
    // 调用后端API
    const response = await axios.post("http://localhost:8000/api/ai/ask/", {
      question: question,
    });

    // 添加AI回复
    messages.value.push({
      role: "ai",
      content: response.data.answer,
    });
  } catch (error) {
    console.error("AI助手请求失败:", error);
    messages.value.push({
      role: "ai",
      content: "抱歉，我遇到了点问题。请稍后再试。",
    });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

// 监听消息变化，自动滚动
watch(messages, scrollToBottom, { deep: true });
</script>

<style scoped>
.ai-assistant {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000;
}

.assistant-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.assistant-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.chat-window {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  padding: 15px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  line-height: 1;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #f8f9fa;
}

.message {
  margin-bottom: 15px;
  padding: 12px 15px;
  border-radius: 18px;
  max-width: 80%;
  line-height: 1.4;
  word-wrap: break-word;
}

.message.user {
  background: #667eea;
  color: white;
  margin-left: auto;
  border-bottom-right-radius: 5px;
}

.message.ai {
  background: white;
  color: #333;
  border: 1px solid #e0e0e0;
  margin-right: auto;
  border-bottom-left-radius: 5px;
}

.message.loading {
  color: #666;
  font-style: italic;
}

.chat-input {
  padding: 15px;
  background: white;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 25px;
  outline: none;
  font-size: 14px;
}

.chat-input input:focus {
  border-color: #667eea;
}

.chat-input button {
  padding: 12px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.3s ease;
}

.chat-input button:hover:not(:disabled) {
  background: #5a67d8;
}

.chat-input button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

/* 滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
</style>
