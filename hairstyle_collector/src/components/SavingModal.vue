<template>
  <transition name="modal-fade">
    <div v-if="show" class="saving-modal-backdrop">
      <div class="saving-modal-card">
        
        <!-- Animated Header Icon -->
        <div class="modal-icon-wrapper" :class="{'is-complete': percentage === 100}">
          <i v-if="percentage < 100" class="fa-solid fa-cloud-arrow-up fa-bounce"></i>
          <i v-else class="fa-solid fa-circle-check"></i>
        </div>

        <h3 class="saving-title">
          {{ percentage === 100 ? (isEditMode ? 'Record Updated!' : 'Record Saved!') : (isEditMode ? 'Updating Hairstyle Record...' : 'Saving New Hairstyle Record...') }}
        </h3>

        <!-- Status Task & Percentage -->
        <div class="status-task-text">{{ currentTask }}</div>

        <!-- Progress Bar -->
        <div class="progress-container">
          <div class="progress-bar-track">
            <div class="progress-bar-fill" :style="{ width: percentage + '%' }"></div>
          </div>
          <div class="progress-percent">{{ percentage }}%</div>
        </div>

        <!-- Step List Tracker -->
        <div class="step-tracker">
          <div class="step-item" :class="{'done': percentage >= 30, 'active': percentage < 80}">
            <i class="fa-solid" :class="percentage >= 80 ? 'fa-circle-check' : (percentage >= 30 ? 'fa-spinner fa-spin' : 'fa-circle')"></i>
            <span>Cloudinary CDN Photo Streaming</span>
          </div>

          <div class="step-item" :class="{'done': percentage >= 90, 'active': percentage >= 80 && percentage < 100}">
            <i class="fa-solid" :class="percentage === 100 ? 'fa-circle-check' : (percentage >= 80 ? 'fa-spinner fa-spin' : 'fa-circle')"></i>
            <span>Firebase Firestore Metadata Sync</span>
          </div>
        </div>

      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  show: { type: Boolean, default: false },
  isEditMode: { type: Boolean, default: false },
  percentage: { type: Number, default: 0 },
  currentTask: { type: String, default: "Saving record..." }
});
</script>

<style scoped>
.saving-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  padding: 1.5rem;
}

.saving-modal-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 2.5rem 2rem;
  max-width: 480px;
  width: 100%;
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: modalScaleUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-icon-wrapper {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #e0e7ff;
  color: #6366f1;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem auto;
  transition: all 0.3s ease;
}

.modal-icon-wrapper.is-complete {
  background: #d1fae5;
  color: #10b981;
}

.saving-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.35rem;
}

.status-task-text {
  font-size: 0.88rem;
  color: #64748b;
  margin-bottom: 1.5rem;
  min-height: 1.4em;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.progress-bar-track {
  flex: 1;
  height: 12px;
  background: #f1f5f9;
  border-radius: 999px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
  border-radius: 999px;
  transition: width 0.25s ease;
}

.progress-percent {
  font-size: 0.95rem;
  font-weight: 800;
  color: #6366f1;
  min-width: 45px;
}

.step-tracker {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem;
  text-align: left;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.82rem;
  color: #94a3b8;
}

.step-item i { font-size: 0.9rem; }

.step-item.active {
  color: #6366f1;
  font-weight: 700;
}

.step-item.done {
  color: #10b981;
  font-weight: 600;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
