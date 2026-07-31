<template>
  <transition name="fade">
    <div v-if="show" class="toast" :class="type">
      {{ message }}
    </div>
  </transition>
</template>

<script setup>
defineProps({
  show: { type: Boolean, default: false },
  message: { type: String, default: "" },
  type: { type: String, default: "info" }
});
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: #0f172a;
  color: #fff;
  padding: 0.85rem 1.5rem;
  border-radius: 10px;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
  font-size: 0.9rem;
  font-weight: 600;
  z-index: 1000;
}

.toast.success { border-left: 4px solid #10b981; }
.toast.error { border-left: 4px solid #ef4444; }
.toast.info { border-left: 4px solid #6366f1; }

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
