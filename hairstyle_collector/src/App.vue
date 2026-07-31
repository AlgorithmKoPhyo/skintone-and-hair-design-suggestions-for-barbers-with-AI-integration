<template>
  <div id="app-container">
    <Navbar 
      :firestore-connected="firestoreConnected"
      :hairstyles-count="hairstylesCount"
      @export-json="exportAllJSON"
    />

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component 
            :is="Component" 
            @notify="notify"
            @refresh-count="updateCount"
          />
        </transition>
      </router-view>
    </main>

    <Toast 
      :show="toastState.show" 
      :message="toastState.message" 
      :type="toastState.type" 
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import Navbar from './components/Navbar.vue';
import Toast from './components/Toast.vue';
import { initFirestore, fetchFromFirestore, isFirestoreReady } from './services/firebase.js';

const firestoreConnected = ref(false);
const hairstylesCount = ref(0);

const toastState = reactive({
  show: false,
  message: "",
  type: "info"
});

const notify = ({ message, type = "info" }) => {
  toastState.message = message;
  toastState.type = type;
  toastState.show = true;
  setTimeout(() => {
    toastState.show = false;
  }, 3500);
};

const updateCount = (count) => {
  hairstylesCount.value = count;
};

onMounted(() => {
  firestoreConnected.value = initFirestore();
});

const exportAllJSON = async () => {
  try {
    let data = [];
    if (isFirestoreReady()) {
      data = await fetchFromFirestore();
    }
    if (!data || data.length === 0) {
      notify({ message: "No records found to export.", type: "error" });
      return;
    }

    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `hairstyles_export_${Date.now()}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();

    notify({ message: "Exported all Firestore records to JSON!", type: "success" });
  } catch (e) {
    notify({ message: "Export failed: " + e.message, type: "error" });
  }
};
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: #FAF8FF;
  background-image: 
    radial-gradient(at 10% 10%, rgba(243, 232, 255, 0.6) 0px, transparent 50%),
    radial-gradient(at 90% 90%, rgba(252, 231, 243, 0.5) 0px, transparent 50%);
  background-attachment: fixed;
  color: #1E1B4B;
  line-height: 1.5;
  min-height: 100vh;
}

.main-content {
  max-width: 1400px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(6px);
}
</style>
