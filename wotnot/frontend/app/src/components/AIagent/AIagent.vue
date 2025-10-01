<script>
import axios from "axios";
import { nextTick } from "vue";

export default {
  data() {
    return {
      messages: [
        { role: "assistant", text: "Hello! How can I assist you today?" }
      ],
      inputMessage: "",
      isConfigMode: false,
      apiKey: localStorage.getItem("apiKey") || "",
    };
  },
  methods: {
    async sendMessage() {
      if (!this.inputMessage.trim()) return;

      // Add user message
      this.messages.push({ role: "user", text: this.inputMessage });

      try {
        const response = await axios.post("http://127.0.0.1:8000/chat", {
          message: this.inputMessage,
        });
        this.messages.push({ role: "assistant", text: response.data.response });
      } catch (error) {
        this.messages.push({ role: "assistant", text: "Error connecting to server" });
      }

      this.inputMessage = "";
      this.scrollToBottom();
    },
    saveApiKey() {
      localStorage.setItem("apiKey", this.apiKey);
      this.isConfigMode = false;
    },
    scrollToBottom() {
      nextTick(() => {
        const chatContainer = this.$refs.chatList;
        if (chatContainer) {
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }
      });
    }
  },
};
</script>

<template>
  <div class="content-section flex flex-col h-screen bg-gray-900 text-white md:ml-64 " >
    <!-- Header -->
    <div class="fixed w-full flex items-center top-0 px-6 py-4 bg-gray-800">
      <div class="text-2xl font-bold">ChatGPT</div>
      <div class="ml-auto text-sm cursor-pointer hover:bg-gray-700 px-3 py-2 rounded-md" @click="isConfigMode = !isConfigMode">
        Settings
      </div>
    </div>

    <!-- Chat Messages -->
    <div ref="chatList" class="flex-1 overflow-y-auto p-4 mt-16 mb-20">
      <div v-for="(msg, index) in messages" :key="index"
        class="p-3 rounded-lg max-w-xs" 
        :class="msg.role === 'user' ? 'bg-blue-600 self-end' : 'bg-gray-700 self-start'">
        {{ msg.text }}
      </div>
    </div>

    <!-- Settings Mode -->
    <div v-if="isConfigMode" class="p-6 bg-gray-800 border-t border-gray-700">
      <div class="text-sm text-gray-400 mb-2">Enter API Key:</div>
      <div class="flex">
        <input v-model="apiKey" class="flex-1 p-2 bg-gray-700 text-white rounded-lg outline-none" type="password" placeholder="sk-xxxxxxxxxx"/>
        <button @click="saveApiKey" class="ml-2 px-4 py-2 bg-green-500 rounded-lg">Save</button>
      </div>
    </div>

    <!-- Input Box -->
    <div v-else class="fixed bottom-0 w-[1350px] p-6 bg-gray-800 border-t border-gray-700 flex items-center">
      <input v-model="inputMessage" @keydown.enter="sendMessage" class="flex-1 p-2 bg-gray-700 text-white rounded-lg outline-none" placeholder="Type a message..."/>
      <button @click="sendMessage" class="ml-2 px-4 py-2 bg-blue-500 rounded-lg">Send</button>
    </div>
  </div>
</template>
