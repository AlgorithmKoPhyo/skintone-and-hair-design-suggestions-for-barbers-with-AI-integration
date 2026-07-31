<template>
  <transition name="modal-fade">
    <div v-if="show" class="image-modal-backdrop" @click.self="$emit('close')">
      <div class="image-modal-content">
        <button class="btn-close-modal" @click="$emit('close')" title="Close (Esc)">&times;</button>
        
        <div class="image-wrapper">
          <img :src="imageUrl" :alt="title" class="preview-full-image">
        </div>

        <div class="modal-caption">
          <h3>{{ title }}</h3>
          <p v-if="subtitle" class="caption-sub">{{ subtitle }}</p>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';

const props = defineProps({
  show: { type: Boolean, default: false },
  imageUrl: { type: String, default: "" },
  title: { type: String, default: "" },
  subtitle: { type: String, default: "" }
});

const emit = defineEmits(['close']);

const handleKeyDown = (e) => {
  if (e.key === "Escape" && props.show) {
    emit('close');
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<style scoped>
/* Bright Light-Themed Image Modal Backdrop & Card */
.image-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  padding: 1.5rem;
}

.image-modal-content {
  position: relative;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  max-width: 850px;
  width: 90%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.75rem;
  box-shadow: 0 20px 40px -10px rgba(124, 58, 237, 0.2);
  overflow: hidden;
  animation: modalScaleUp 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.btn-close-modal {
  position: absolute;
  top: 1rem;
  right: 1.25rem;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #334155;
  font-size: 1.8rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  z-index: 10;
}

.btn-close-modal:hover {
  background: #ef4444;
  color: #ffffff;
  border-color: #ef4444;
  transform: scale(1.1);
}

.image-wrapper {
  width: 100%;
  max-height: 70vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  border-radius: 16px;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
}

.preview-full-image {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
  border-radius: 14px;
}

.modal-caption {
  margin-top: 1.25rem;
  text-align: center;
  color: #0f172a;
}

.modal-caption h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
}

.caption-sub {
  font-size: 0.85rem;
  color: #64748b;
  margin-top: 0.2rem;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
