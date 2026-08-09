<template>
  <header class="app-header">
    <div class="header-container">
      <div class="brand">
        <i class="fa-solid fa-scissors brand-icon"></i>
        <div>
          <h1>StyleMe Data Collector</h1>
        </div>
      </div>

      <div class="header-actions">
        <div class="status-pill" :class="firestoreConnected ? 'status-connected' : 'status-demo'">
          <span class="dot"></span>
          <span>{{ firestoreConnected ? 'Firestore DB Connected | Cloudinary Active' : 'Firestore Disconnected' }}</span>
        </div>
        
        <!-- Solid Color Export Button (Solid #7C3AED - No Gradient) -->
        <button @click="$emit('export-json')" class="btn-export-json">
          <i class="fa-solid fa-file-arrow-down icon-download"></i>
          <span>Export to JSON</span>
          <span class="btn-badge">JSON</span>
        </button>
      </div>
    </div>

    <!-- Vue Router Navigation Tabs -->
    <nav class="app-nav">
      <div class="nav-container">
        <router-link to="/catalog" class="nav-tab" active-class="active">
          <i class="fa-solid fa-table"></i> Data Catalog ({{ hairstylesCount }})
        </router-link>
        <router-link to="/create" class="nav-tab" active-class="active">
          <i class="fa-solid fa-plus-circle"></i> Add New Hairstyle
        </router-link>
      </div>
    </nav>
  </header>
</template>

<script setup>
defineProps({
  firestoreConnected: { type: Boolean, default: false },
  hairstylesCount: { type: Number, default: 0 }
});

defineEmits(['export-json']);
</script>

<style scoped>
.app-header {
  background: #1E1B4B;
  color: #fff;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-icon {
  font-size: 1.8rem;
  color: #EC4899;
  background: rgba(255,255,255,0.08);
  padding: 0.75rem;
  border-radius: 14px;
  border: 1px solid rgba(236, 72, 153, 0.25);
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.2);
}

.brand h1 {
  font-family: 'Outfit', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #ffffff;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

/* Status Pill */
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.45rem 0.95rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-pill .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-demo {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}
.status-demo .dot { background: #fbbf24; }

.status-connected {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}
.status-connected .dot { background: #34d399; }

/* Solid Color Export Button (Solid #7C3AED) */
.btn-export-json {
  background: #7C3AED;
  color: #ffffff;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 14px;
  font-family: inherit;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn-export-json:hover {
  background: #6D28D9;
  box-shadow: 0 6px 18px rgba(124, 58, 237, 0.35);
  transform: translateY(-2px);
}

.btn-export-json:active {
  transform: translateY(0);
}

.icon-download {
  font-size: 0.95rem;
  transition: transform 0.2s ease;
}

.btn-export-json:hover .icon-download {
  transform: translateY(2px);
}

.btn-badge {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
  font-size: 0.68rem;
  font-weight: 800;
  padding: 0.15rem 0.45rem;
  border-radius: 6px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* Navigation Tabs */
.app-nav {
  background: #17153B;
  border-top: 1px solid rgba(255,255,255,0.08);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  gap: 0.5rem;
}

.nav-tab {
  background: none;
  border: none;
  color: #94A3B8;
  padding: 0.85rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-bottom: 3px solid transparent;
  text-decoration: none;
  transition: all 0.2s ease;
}

.nav-tab:hover {
  color: #fff;
}

.nav-tab.active {
  color: #C084FC;
  border-bottom-color: #7C3AED;
}
</style>
