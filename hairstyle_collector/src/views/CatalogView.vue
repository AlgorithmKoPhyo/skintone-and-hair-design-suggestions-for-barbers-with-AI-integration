<template>
  <section class="catalog-pane">
    <!-- Top Filter & Search Toolbar -->
    <div class="catalog-toolbar">
      <div class="search-box">
        <i class="fa-solid fa-magnifying-glass"></i>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search hairstyles by name, slug, face shape, tags..."
        >
      </div>

      <div class="filter-group">
        <!-- Custom Dropdown 1: Binary Usage Status -->
        <div class="custom-select-wrapper">
          <i class="fa-solid fa-layer-group select-icon"></i>
          <select v-model="selectedStatus" class="custom-select">
            <option value="all">All Statuses</option>
            <option value="1">Published</option>
            <option value="0">Draft</option>
          </select>
          <i class="fa-solid fa-chevron-down arrow-icon"></i>
        </div>

        <!-- Custom Dropdown 2: Face Shape -->
        <div class="custom-select-wrapper">
          <i class="fa-solid fa-user-gear select-icon"></i>
          <select v-model="selectedShape" class="custom-select">
            <option value="all">All Face Shapes</option>
            <option value="oval">Oval Face</option>
            <option value="round">Round Face</option>
            <option value="square">Square Face</option>
            <option value="heart">Heart Face</option>
            <option value="diamond">Diamond Face</option>
            <option value="oblong">Oblong Face</option>
          </select>
          <i class="fa-solid fa-chevron-down arrow-icon"></i>
        </div>

        <!-- Custom Dropdown 3: Gender -->
        <div class="custom-select-wrapper">
          <i class="fa-solid fa-mars-female select-icon"></i>
          <select v-model="selectedGender" class="custom-select">
            <option value="all">All Genders</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
          <i class="fa-solid fa-chevron-down arrow-icon"></i>
        </div>

        <router-link to="/create" class="btn btn-primary btn-add">
          <i class="fa-solid fa-plus"></i> Add Hairstyle
        </router-link>
      </div>
    </div>

    <!-- Loading Spinner State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner-icon">
        <i class="fa-solid fa-circle-notch fa-spin"></i>
      </div>
      <p>Loading catalog from Firestore...</p>
    </div>

    <!-- Main Data Table Container -->
    <div v-else class="catalog-table-container">
      <table class="modern-catalog-table">
        <thead>
          <tr>
            <th class="th-main">Hairstyle & Variation</th>
            <th class="th-shape">Status & Badges</th>
            <th class="th-specs">Hair Specs</th>
            <th class="th-angles">4 Angle Photos</th>
            <th class="th-details">Description & Matrix</th>
            <th class="th-actions" style="text-align: right;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <!-- Empty State -->
          <tr v-if="paginatedHairstyles.length === 0">
            <td colspan="6" class="empty-cell">
              <div class="empty-box">
                <i class="fa-solid fa-folder-open empty-icon"></i>
                <h3>No Hairstyles Found</h3>
                <p>Try adjusting your search query or filters above.</p>
              </div>
            </td>
          </tr>

          <!-- Data Rows Loop -->
          <template v-for="item in paginatedHairstyles" :key="item.id">
            <tr class="main-table-row">
              
              <!-- Column 1: Hairstyle & Variation -->
              <td class="td-cell cell-identity">
                <div class="identity-wrapper">
                  <div class="cover-avatar" @click="openImageModal(item.main_img, item.name, 'Main Cover / Thumbnail')" title="Click to enlarge photo">
                    <img :src="item.main_img || 'https://images.unsplash.com/photo-1622286342621-4bd786c2447c?w=300'" :alt="item.name">
                    <span class="zoom-pill"><i class="fa-solid fa-magnifying-glass-plus"></i></span>
                  </div>
                  <div class="identity-info">
                    <div class="hairstyles-title">{{ item.name }}</div>
                    <div class="hairstyles-slug"><code>{{ item.slug }}</code></div>
                    <div v-if="item.category" class="hairstyles-cat" style="font-size: 0.78rem; color: #7C3AED; font-weight: 600; margin-top: 2px;">
                      <i class="fa-solid fa-folder-tree"></i> {{ item.category }}
                    </div>
                    <div v-if="item.variation_name" class="hairstyles-var">
                      <i class="fa-solid fa-code-branch"></i> {{ item.variation_name }}
                    </div>
                  </div>
                </div>
              </td>

              <!-- Column 2: Binary Status & Badges -->
              <td class="td-cell cell-badges">
                <div class="badge-group">
                  <span v-if="item.status === 1 || item.status === '1' || item.status === 'main_page'" class="badge-item badge-status-main" title="Published Record - Locked from Editing">
                    <i class="fa-solid fa-lock"></i> Published
                  </span>
                  <span v-else class="badge-item badge-status-draft">
                    <i class="fa-solid fa-file-pen"></i> Draft
                  </span>

                  <span class="badge-item badge-faceshape">
                    <i class="fa-solid fa-user-gear"></i> {{ item.faceshape }} face
                  </span>
                  <span class="badge-item badge-gender">
                    <i class="fa-solid fa-mars-female"></i> {{ item.gender }}
                  </span>
                  <span v-if="item.score_badge" class="badge-item badge-score">
                    <i class="fa-solid fa-bolt"></i> {{ item.score_badge }}
                  </span>
                  <span v-if="item.shape_badge" class="badge-item badge-tag">
                    {{ item.shape_badge }}
                  </span>
                </div>
              </td>

              <!-- Column 3: Hair Specs -->
              <td class="td-cell cell-specs">
                <div class="specs-grid">
                  <div class="spec-row"><i class="fa-solid fa-ruler-vertical"></i> <span>{{ item.hair_length || '-' }}</span></div>
                  <div class="spec-row"><i class="fa-solid fa-wand-magic-sparkles"></i> <span>{{ item.hair_texture || '-' }}</span></div>
                  <div class="spec-row"><i class="fa-solid fa-clock"></i> <span>{{ item.styling_time || '-' }}</span></div>
                  <div class="spec-row"><i class="fa-solid fa-shield-halved"></i> <span>{{ item.maintenance || '-' }}</span></div>
                </div>
              </td>

              <!-- Column 4: 4 Angle Photos -->
              <td class="td-cell cell-angles">
                <div class="angle-grid">
                  <div 
                    v-for="(angle, idx) in (item.angles || [])" 
                    :key="idx" 
                    class="angle-thumb-box"
                    @click="openImageModal(angle.img || item.main_img, item.name, angle.name + ' View')"
                    :title="'Click to enlarge ' + angle.name + ' photo'"
                  >
                    <img :src="angle.img || item.main_img" :alt="angle.name">
                    <span class="angle-caption">{{ angle.name }}</span>
                  </div>
                </div>
              </td>

              <!-- Column 5: Description & Matrix Toggle -->
              <td class="td-cell cell-details">
                <div class="details-wrapper">
                  <p class="description-text">{{ item.description }}</p>
                  <button @click="toggleExpand(item.id)" class="btn-matrix-toggle">
                    <i class="fa-solid" :class="expandedRows[item.id] ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
                    <span>{{ expandedRows[item.id] ? 'Hide Details' : 'View Checklist & Matrix' }}</span>
                  </button>
                </div>
              </td>

              <!-- Column 6: Actions (Edit Locked for Published status: 1) -->
              <td class="td-cell cell-actions" style="text-align: right;">
                <div class="actions-wrapper">
                  <button 
                    v-if="item.status === 1 || item.status === '1' || item.status === 'main_page'" 
                    class="btn-action btn-edit btn-locked" 
                    disabled 
                    title="Published records (status: 1) are locked and cannot be edited"
                  >
                    <i class="fa-solid fa-lock"></i>
                    <span>Locked</span>
                  </button>
                  <button 
                    v-else 
                    @click="editHairstyle(item.id)" 
                    class="btn-action btn-edit" 
                    title="Edit Record"
                  >
                    <i class="fa-solid fa-pen-to-square"></i>
                    <span>Edit</span>
                  </button>

                  <button @click="deleteHairstyle(item.id)" class="btn-action btn-delete" title="Delete Record">
                    <i class="fa-solid fa-trash-can"></i>
                    <span>Delete</span>
                  </button>
                </div>
              </td>

            </tr>

            <!-- Expandable Details & Matrix Drawer Row -->
            <tr v-if="expandedRows[item.id]" :key="'drawer-' + item.id" class="drawer-table-row">
              <td colspan="6" class="drawer-td">
                <div class="drawer-container">
                  
                  <!-- Drawer Box 1: Recommendation Reasons -->
                  <div v-if="item.reasons && item.reasons.length" class="drawer-box">
                    <div class="drawer-box-header">
                      <i class="fa-solid fa-list-check"></i> Recommendation Reasons
                    </div>
                    <ul class="drawer-list">
                      <li v-for="(r, rIdx) in item.reasons" :key="rIdx">
                        <i class="fa-solid fa-check"></i> <span>{{ r }}</span>
                      </li>
                    </ul>
                  </div>

                  <!-- Drawer Box 2: Care & Styling Tips -->
                  <div v-if="item.tips && item.tips.length" class="drawer-box">
                    <div class="drawer-box-header">
                      <i class="fa-solid fa-lightbulb"></i> Styling & Care Tips
                    </div>
                    <ul class="drawer-list tips-list">
                      <li v-for="(t, tIdx) in item.tips" :key="tIdx">
                        <i class="fa-solid fa-star"></i> <span>{{ t }}</span>
                      </li>
                    </ul>
                  </div>

                  <!-- Drawer Box 3: Suitability Matrix Scores -->
                  <div class="drawer-box matrix-box">
                    <div class="drawer-box-header">
                      <i class="fa-solid fa-chart-pie"></i> Face Shape Suitability Matrix
                    </div>
                    <div class="matrix-grid">
                      <div v-for="(suit, sIdx) in (item.suitability || [])" :key="sIdx" class="matrix-chip">
                        <span class="m-label">{{ suit.shape }}:</span>
                        <span class="m-value">{{ suit.score || '-' }}</span>
                      </div>
                    </div>
                  </div>

                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>

      <!-- Bottom Pagination Controls -->
      <div v-if="filteredHairstyles.length > 0" class="pagination-footer">
        <div class="pagination-count">
          Showing <strong>{{ pageStartIdx + 1 }}</strong> - <strong>{{ pageEndIdx }}</strong> of <strong>{{ filteredHairstyles.length }}</strong> records
        </div>

        <div class="pagination-right">
          <!-- Page Size Dropdown -->
          <div class="page-size-box">
            <span>Show:</span>
            <select v-model.number="pageSize" @change="currentPage = 1">
              <option :value="5">5 per page</option>
              <option :value="10">10 per page</option>
              <option :value="25">25 per page</option>
              <option :value="50">50 per page</option>
            </select>
          </div>

          <!-- Page Buttons -->
          <div class="page-nav-group">
            <button @click="currentPage--" :disabled="currentPage === 1" class="page-nav-btn">
              <i class="fa-solid fa-chevron-left"></i>
            </button>

            <button 
              v-for="page in visiblePageNumbers" 
              :key="page"
              @click="currentPage = page"
              class="page-num-btn"
              :class="{'active': currentPage === page}"
            >
              {{ page }}
            </button>

            <button @click="currentPage++" :disabled="currentPage >= totalPages" class="page-nav-btn">
              <i class="fa-solid fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Image Lightbox Modal -->
    <ImageModal 
      :show="modalState.show"
      :image-url="modalState.url"
      :title="modalState.title"
      :subtitle="modalState.subtitle"
      @close="modalState.show = false"
    />
  </section>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { fetchFromFirestore, deleteFromFirestore, isFirestoreReady } from '../services/firebase.js';
import ImageModal from '../components/ImageModal.vue';

const emit = defineEmits(['notify', 'refresh-count']);
const router = useRouter();

const hairstyles = ref([]);
const searchQuery = ref("");
const selectedStatus = ref("all");
const selectedShape = ref("all");
const selectedGender = ref("all");
const isLoading = ref(true);
const expandedRows = reactive({});

// Pagination State
const currentPage = ref(1);
const pageSize = ref(10);

// Image Lightbox Modal State
const modalState = reactive({
  show: false,
  url: "",
  title: "",
  subtitle: ""
});

const openImageModal = (url, title, subtitle) => {
  if (!url) return;
  modalState.url = url;
  modalState.title = title;
  modalState.subtitle = subtitle;
  modalState.show = true;
};

const loadData = async () => {
  isLoading.value = true;
  try {
    if (isFirestoreReady()) {
      hairstyles.value = await fetchFromFirestore();
    }
    emit("refresh-count", hairstyles.value.length);
  } catch (err) {
    console.error("Error loading catalog:", err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(loadData);

const toggleExpand = (id) => {
  expandedRows[id] = !expandedRows[id];
};

const filteredHairstyles = computed(() => {
  const q = searchQuery.value.toLowerCase().trim();
  return hairstyles.value.filter(item => {
    const matchesSearch = !q || 
      item.name?.toLowerCase().includes(q) || 
      item.slug?.toLowerCase().includes(q) ||
      item.category?.toLowerCase().includes(q) ||
      item.faceshape?.toLowerCase().includes(q) ||
      item.description?.toLowerCase().includes(q);

    const isPublished = item.status === 1 || item.status === "1" || item.status === "main_page";
    const matchesStatus = selectedStatus.value === "all" || 
      (selectedStatus.value === "1" && isPublished) ||
      (selectedStatus.value === "0" && !isPublished);

    const matchesShape = selectedShape.value === "all" || item.faceshape === selectedShape.value;
    const matchesGender = selectedGender.value === "all" || item.gender === selectedGender.value;

    return matchesSearch && matchesStatus && matchesShape && matchesGender;
  });
});

// Auto reset pagination when filters change
watch([searchQuery, selectedStatus, selectedShape, selectedGender], () => {
  currentPage.value = 1;
});

const totalPages = computed(() => Math.ceil(filteredHairstyles.value.length / pageSize.value) || 1);
const pageStartIdx = computed(() => (currentPage.value - 1) * pageSize.value);
const pageEndIdx = computed(() => Math.min(currentPage.value * pageSize.value, filteredHairstyles.value.length));

const paginatedHairstyles = computed(() => {
  return filteredHairstyles.value.slice(pageStartIdx.value, pageEndIdx.value);
});

const visiblePageNumbers = computed(() => {
  const pages = [];
  const total = totalPages.value;
  const curr = currentPage.value;
  let start = Math.max(1, curr - 2);
  let end = Math.min(total, curr + 2);
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

const editHairstyle = (id) => {
  const targetItem = hairstyles.value.find(h => h.id === id);
  if (targetItem && (targetItem.status === 1 || targetItem.status === "1" || targetItem.status === "main_page")) {
    emit("notify", { message: "Published records (status: 1) are locked from editing.", type: "error" });
    return;
  }
  router.push(`/edit/${id}`);
};

const deleteHairstyle = async (id) => {
  if (confirm("Are you sure you want to delete this hairstyle record?")) {
    try {
      if (isFirestoreReady()) {
        await deleteFromFirestore(id);
      }
      emit("notify", { message: "Record deleted successfully.", type: "info" });
      await loadData();
    } catch (err) {
      emit("notify", { message: "Error deleting: " + err.message, type: "error" });
    }
  }
};
</script>

<style scoped>
.catalog-pane {
  animation: fadeIn 0.3s ease;
}

/* Toolbar Controls */
.catalog-toolbar {
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 20px;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 10px 30px -5px rgba(124, 58, 237, 0.05);
}

.search-box {
  position: relative;
  flex: 1;
}

.search-box i {
  position: absolute;
  left: 1.1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 0.95rem;
}

.search-box input {
  width: 100%;
  padding: 0.7rem 1rem 0.7rem 2.7rem;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.search-box input:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15);
}

.filter-group {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.custom-select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.select-icon {
  position: absolute;
  left: 0.9rem;
  color: #7C3AED;
  font-size: 0.85rem;
  pointer-events: none;
  z-index: 2;
}

.arrow-icon {
  position: absolute;
  right: 0.9rem;
  color: #94a3b8;
  font-size: 0.75rem;
  pointer-events: none;
  z-index: 2;
}

.custom-select {
  appearance: none;
  padding: 0.7rem 2.2rem 0.7rem 2.4rem;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  font-size: 0.85rem;
  background: #ffffff;
  font-weight: 600;
  color: #1E1B4B;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}

.custom-select:hover {
  border-color: #7C3AED;
  background: #FAF8FF;
}

.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  color: #64748b;
}

.spinner-icon {
  font-size: 2.5rem;
  color: #7C3AED;
  margin-bottom: 1rem;
}

/* Modern Redesigned Table Structure with Main Site Palette */
.catalog-table-container {
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px -5px rgba(124, 58, 237, 0.06);
}

.modern-catalog-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.modern-catalog-table th {
  background: #FAF8FF;
  color: #1E1B4B;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 1.1rem 1.25rem;
  border-bottom: 2px solid #EDE9FE;
}

.main-table-row {
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.15s ease;
}

.main-table-row:hover {
  background: #FAF8FF;
}

.td-cell {
  padding: 1.1rem 1.25rem;
  vertical-align: middle;
}

/* Col 1: Identity */
.identity-wrapper {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.cover-avatar {
  position: relative;
  width: 58px;
  height: 58px;
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  flex-shrink: 0;
  border: 1px solid #e2e8f0;
}

.cover-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.25s ease;
}

.cover-avatar:hover img {
  transform: scale(1.1);
}

.zoom-pill {
  position: absolute;
  right: 4px;
  bottom: 4px;
  background: rgba(124, 58, 237, 0.9);
  color: #fff;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 0.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hairstyles-title {
  font-weight: 700;
  font-size: 0.95rem;
  color: #1E1B4B;
}

.hairstyles-slug code {
  font-size: 0.75rem;
  background: #EDE9FE;
  color: #6D28D9;
  padding: 0.15rem 0.45rem;
  border-radius: 6px;
  font-family: monospace;
}

.hairstyles-var {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 0.15rem;
}

/* Col 2: Badges & Status */
.badge-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  align-items: flex-start;
}

.badge-item {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.65rem;
  border-radius: 999px;
}

.badge-status-main { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.badge-status-draft { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }

.badge-faceshape { background: #F3E8FF; color: #7C3AED; }
.badge-gender { background: #F1F5F9; color: #475569; }
.badge-score { background: #ECFDF5; color: #059669; }
.badge-tag { background: #FCE7F3; color: #DB2777; }

/* Col 3: Hair Specs */
.specs-grid {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.spec-row {
  font-size: 0.78rem;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.spec-row i { color: #7C3AED; font-size: 0.75rem; width: 14px; text-align: center; }

/* Col 4: 4 Angle Photos */
.angle-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.35rem;
}

.angle-thumb-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.angle-thumb-box img {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  object-fit: cover;
  border: 1px solid #cbd5e1;
  transition: all 0.2s ease;
}

.angle-thumb-box:hover img {
  transform: scale(1.18);
  border-color: #7C3AED;
  box-shadow: 0 4px 10px rgba(124, 58, 237, 0.25);
  z-index: 10;
}

.angle-caption {
  font-size: 0.62rem;
  color: #64748b;
  margin-top: 0.1rem;
}

/* Col 5: Description & Matrix Toggle */
.details-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.description-text {
  font-size: 0.8rem;
  color: #475569;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.btn-matrix-toggle {
  background: none;
  border: none;
  color: #7C3AED;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0;
}

.btn-matrix-toggle:hover {
  text-decoration: underline;
}

/* Col 6: Actions */
.actions-wrapper {
  display: inline-flex;
  gap: 0.5rem;
}

.btn-action {
  border: none;
  padding: 0.45rem 0.85rem;
  border-radius: 10px;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.2s ease;
}

.btn-edit {
  background: #FEF3C7;
  color: #B45309;
  border: 1px solid #FDE68A;
}

.btn-edit:hover:not(:disabled) {
  background: #F59E0B;
  color: #ffffff;
  box-shadow: 0 4px 10px rgba(245, 158, 11, 0.3);
}

.btn-locked {
  background: #f1f5f9;
  color: #94a3b8;
  border: 1px solid #e2e8f0;
  cursor: not-allowed;
}

.btn-delete {
  background: #FEE2E2;
  color: #B91C1C;
  border: 1px solid #FCA5A5;
}

.btn-delete:hover {
  background: #EF4444;
  color: #ffffff;
  box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3);
}

/* Expandable Drawer Row */
.drawer-td {
  background: #FAF8FF;
  padding: 1.25rem;
  border-bottom: 2px solid #EDE9FE;
}

.drawer-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1.2fr;
  gap: 1.25rem;
}

.drawer-box {
  background: #ffffff;
  border: 1px solid #EDE9FE;
  border-radius: 14px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.04);
}

.drawer-box-header {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1E1B4B;
  margin-bottom: 0.6rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.drawer-box-header i { color: #7C3AED; }

.drawer-list {
  list-style: none;
  font-size: 0.78rem;
  color: #475569;
}

.drawer-list li {
  margin-bottom: 0.3rem;
  display: flex;
  align-items: flex-start;
  gap: 0.4rem;
}

.drawer-list li i { color: #10B981; margin-top: 0.15rem; }
.tips-list li i { color: #F59E0B; }

.matrix-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.4rem;
}

.matrix-chip {
  background: #FAF8FF;
  padding: 0.35rem 0.65rem;
  border-radius: 8px;
  border: 1px solid #EDE9FE;
  font-size: 0.75rem;
  display: flex;
  justify-content: space-between;
}

.m-label { color: #64748b; }
.m-value { font-weight: 700; color: #1E1B4B; }

/* Empty State */
.empty-cell {
  padding: 4rem 2rem;
  text-align: center;
}

.empty-box {
  color: #94a3b8;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 0.75rem;
  color: #cbd5e1;
}

/* Footer Pagination */
.pagination-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: #FAF8FF;
  border-top: 1px solid #EDE9FE;
}

.pagination-count {
  font-size: 0.85rem;
  color: #64748b;
}

.pagination-right {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.page-size-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #475569;
}

.page-size-box select {
  padding: 0.35rem 0.6rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.82rem;
  background: #ffffff;
  color: #1E1B4B;
}

.page-nav-group {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.page-nav-btn, .page-num-btn {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #334155;
  padding: 0.4rem 0.75rem;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-nav-btn:hover:not(:disabled),
.page-num-btn:hover {
  border-color: #7C3AED;
  color: #7C3AED;
  background: #F3E8FF;
}

.page-nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-num-btn.active {
  background: #7C3AED;
  color: #ffffff;
  border-color: #7C3AED;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

.btn {
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.65rem 1.25rem;
  border-radius: 12px;
  border: 1px solid transparent;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  text-decoration: none;
}

.btn-primary { 
  background: #7C3AED; 
  color: #ffffff; 
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
}

.btn-primary:hover { 
  background: #6D28D9; 
  box-shadow: 0 6px 18px rgba(124, 58, 237, 0.35); 
}
</style>
