<template>
  <section class="form-pane">
    <form @submit.prevent="handleSubmit" class="data-form">

      <!-- Locked Warning Banner if record is Main Page -->
      <div v-if="isLockedFromEdit" class="locked-banner">
        <i class="fa-solid fa-lock lock-banner-icon"></i>
        <div>
          <h3>Main Page Record - Locked from Editing</h3>
          <p>This record is marked for <strong>Main Page</strong> usage. Main Page records are protected and cannot be edited in the Data Collector.</p>
        </div>
      </div>

      <!-- Loading State for Edit Record Fetch -->
      <div v-if="isLoadingRecord" class="loading-state">
        <div class="spinner-icon">
          <i class="fa-solid fa-circle-notch fa-spin"></i>
        </div>
        <p>Fetching hairstyle data from Firestore...</p>
      </div>

      <template v-else>
        <!-- Section 1: Basic Identifiers -->
        <div class="form-card" :class="{'form-disabled': isSubmitting || isLockedFromEdit}">
          <div class="card-title"><i class="fa-solid fa-id-card"></i> 1. Basic Information</div>
          <div class="form-grid col-3">
            
            <div class="form-group">
              <label>Usage Status <span class="required">*</span></label>
              <div class="custom-select-wrapper">
                <i class="fa-solid fa-layer-group select-icon"></i>
                <select v-model="formData.status" :disabled="isSubmitting || isLockedFromEdit" class="custom-select">
                  <option value="draft">Draft (Editable)</option>
                  <option value="main_page">Main Page (Locked once saved)</option>
                </select>
                <i class="fa-solid fa-chevron-down arrow-icon"></i>
              </div>
            </div>

            <div class="form-group" :class="{'has-error': errors.name}">
              <label>Hairstyle Name <span class="required">*</span></label>
              <input type="text" v-model="formData.name" @input="onNameInput" :disabled="isSubmitting || isLockedFromEdit" placeholder="e.g. Classic Side Part">
              <span v-if="errors.name" class="error-msg">{{ errors.name }}</span>
            </div>

            <div class="form-group" :class="{'has-error': errors.slug}">
              <label>URL Slug <span class="required">*</span></label>
              <input type="text" v-model="formData.slug" :disabled="isSubmitting || isLockedFromEdit" placeholder="e.g. classic_side_part">
              <span v-if="errors.slug" class="error-msg">{{ errors.slug }}</span>
            </div>

            <div class="form-group">
              <label>Variation Name</label>
              <input type="text" v-model="formData.variation_name" :disabled="isSubmitting || isLockedFromEdit" placeholder="e.g. Low Taper Side Part">
            </div>

            <div class="form-group" :class="{'has-error': errors.faceshape}">
              <label>Primary Face Shape <span class="required">*</span></label>
              <div class="custom-select-wrapper">
                <i class="fa-solid fa-user-gear select-icon"></i>
                <select v-model="formData.faceshape" :disabled="isSubmitting || isLockedFromEdit" class="custom-select">
                  <option value="oval">Oval Face</option>
                  <option value="round">Round Face</option>
                  <option value="square">Square Face</option>
                  <option value="heart">Heart Face</option>
                  <option value="diamond">Diamond Face</option>
                  <option value="oblong">Oblong Face</option>
                </select>
                <i class="fa-solid fa-chevron-down arrow-icon"></i>
              </div>
              <span v-if="errors.faceshape" class="error-msg">{{ errors.faceshape }}</span>
            </div>

            <div class="form-group">
              <label>Gender Target <span class="required">*</span></label>
              <div class="custom-select-wrapper">
                <i class="fa-solid fa-mars-female select-icon"></i>
                <select v-model="formData.gender" :disabled="isSubmitting || isLockedFromEdit" class="custom-select">
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
                <i class="fa-solid fa-chevron-down arrow-icon"></i>
              </div>
            </div>

            <div class="form-group">
              <label>Short Tagline / Catchphrase</label>
              <input type="text" v-model="formData.tagline" :disabled="isSubmitting || isLockedFromEdit" placeholder="e.g. Timeless side-parted cut with clean tapers">
            </div>
          </div>
        </div>

        <!-- Section 2: Display Badges & Hair Specs -->
        <div class="form-card" :class="{'form-disabled': isSubmitting || isLockedFromEdit}">
          <div class="card-title"><i class="fa-solid fa-sliders"></i> 2. Badges & Hair Specifications</div>
          <div class="form-grid col-4">
            <div class="form-group">
              <label>Shape Badge Text</label>
              <input type="text" v-model="formData.shape_badge" :disabled="isSubmitting || isLockedFromEdit" placeholder="e.g. Ideal for Oval Face">
            </div>

            <div class="form-group">
              <label>Match Score Badge</label>
              <input type="text" v-model="formData.score_badge" :disabled="isSubmitting || isLockedFromEdit" placeholder="e.g. 95% Match">
            </div>

            <div class="form-group">
              <label>Hair Length</label>
              <div class="custom-select-wrapper">
                <i class="fa-solid fa-ruler-vertical select-icon"></i>
                <select v-model="formData.hair_length" :disabled="isSubmitting || isLockedFromEdit" class="custom-select">
                  <option value="Very Short">Very Short</option>
                  <option value="Short">Short</option>
                  <option value="Chin Length">Chin Length</option>
                  <option value="Medium">Medium</option>
                  <option value="Shoulder Length">Shoulder Length</option>
                  <option value="Long">Long</option>
                </select>
                <i class="fa-solid fa-chevron-down arrow-icon"></i>
              </div>
            </div>

            <div class="form-group">
              <label>Hair Texture</label>
              <div class="custom-select-wrapper">
                <i class="fa-solid fa-wand-magic-sparkles select-icon"></i>
                <select v-model="formData.hair_texture" :disabled="isSubmitting || isLockedFromEdit" class="custom-select">
                  <option value="Straight / Soft Waves">Straight / Soft Waves</option>
                  <option value="Straight">Straight</option>
                  <option value="Wavy">Wavy</option>
                  <option value="Curly">Curly</option>
                  <option value="Coily">Coily</option>
                  <option value="Textured">Textured</option>
                </select>
                <i class="fa-solid fa-chevron-down arrow-icon"></i>
              </div>
            </div>

            <div class="form-group">
              <label>Daily Styling Time</label>
              <input type="text" v-model="formData.styling_time" :disabled="isSubmitting || isLockedFromEdit" placeholder="e.g. 10 - 15 mins">
            </div>

            <div class="form-group">
              <label>Maintenance Level</label>
              <div class="custom-select-wrapper">
                <i class="fa-solid fa-shield-halved select-icon"></i>
                <select v-model="formData.maintenance" :disabled="isSubmitting || isLockedFromEdit" class="custom-select">
                  <option value="Easy">Easy</option>
                  <option value="Moderate">Moderate</option>
                  <option value="High">High</option>
                </select>
                <i class="fa-solid fa-chevron-down arrow-icon"></i>
              </div>
            </div>
          </div>
        </div>

        <!-- Section 3: Multi-Angle Image Uploaders & Direct Cloudinary Uploads -->
        <div class="form-card" :class="{'form-disabled': isSubmitting || isLockedFromEdit}">
          <div class="card-title"><i class="fa-solid fa-camera"></i> 3. Cover & Multi-Angle Image Uploads</div>
          <p class="section-desc">Drop new image files or paste CDN URLs to update photos directly on Cloudinary CDN.</p>

          <div class="upload-grid">
            <div v-for="angle in angleTypes" :key="angle.key" class="upload-box">
              <div class="upload-label"><i :class="angle.icon"></i> {{ angle.label }}</div>
              
              <div class="dropzone" :class="{'is-disabled': isSubmitting || isLockedFromEdit}" @dragover.prevent @drop.prevent="onDropFile($event, angle.key)">
                <input type="file" accept="image/*" :disabled="isSubmitting || isLockedFromEdit" @change="onSelectFile($event, angle.key)">
                <div class="dropzone-content">
                  <i class="fa-solid fa-cloud-arrow-up"></i>
                  <span>Click or Drag Photo</span>
                </div>
                <img v-if="previews[angle.key]" :src="previews[angle.key]" class="img-preview has-image" alt="Preview">
              </div>

              <input type="text" v-model="imageUrls[angle.key]" :disabled="isSubmitting || isLockedFromEdit" placeholder="Or paste Image URL" class="url-override">
            </div>
          </div>
        </div>

        <!-- Section 4: Detailed Description & Recommendation Content -->
        <div class="form-card" :class="{'form-disabled': isSubmitting || isLockedFromEdit}">
          <div class="card-title"><i class="fa-solid fa-paragraph"></i> 4. Detailed Description & Recommendation Content</div>

          <div class="form-group margin-bottom" :class="{'has-error': errors.description}">
            <label>Full Hairstyle Description <span class="required">*</span></label>
            <textarea v-model="formData.description" :disabled="isSubmitting || isLockedFromEdit" rows="4" placeholder="Comprehensive description of cut geometry, styling tips..." required></textarea>
            <span v-if="errors.description" class="error-msg">{{ errors.description }}</span>
          </div>

          <!-- Recommendation Reasons Checklist -->
          <div class="form-group margin-bottom">
            <div class="label-with-btn">
              <label><i class="fa-solid fa-list-check"></i> Recommendation Reasons Checklist</label>
              <button type="button" @click="addReason" :disabled="isSubmitting || isLockedFromEdit" class="btn btn-xs btn-secondary">
                <i class="fa-solid fa-plus"></i> Add Point
              </button>
            </div>
            <div class="dynamic-list-inputs">
              <div v-for="(reason, idx) in formData.reasons" :key="idx" class="dynamic-row">
                <input type="text" v-model="formData.reasons[idx]" :disabled="isSubmitting || isLockedFromEdit" placeholder="Enter reason point..." class="dynamic-input">
                <button type="button" @click="removeReason(idx)" :disabled="isSubmitting || isLockedFromEdit" class="btn btn-xs btn-danger"><i class="fa-solid fa-xmark"></i></button>
              </div>
            </div>
          </div>

          <!-- Suitability Matrix Scores -->
          <div class="form-group margin-bottom">
            <label><i class="fa-solid fa-chart-pie"></i> Face Shape Match Scores (Suitability Matrix)</label>
            <div class="form-grid col-3 margin-top-sm">
              <div v-for="shape in faceShapeKeys" :key="shape.key" class="score-input-group">
                <span>{{ shape.label }}:</span>
                <input type="text" v-model="formData.scores[shape.key]" :disabled="isSubmitting || isLockedFromEdit" placeholder="e.g. 95% (Ideal)">
              </div>
            </div>
          </div>

          <!-- Styling & Care Tips -->
          <div class="form-group">
            <div class="label-with-btn">
              <label><i class="fa-solid fa-lightbulb"></i> Styling & Care Tips</label>
              <button type="button" @click="addTip" :disabled="isSubmitting || isLockedFromEdit" class="btn btn-xs btn-secondary">
                <i class="fa-solid fa-plus"></i> Add Tip
              </button>
            </div>
            <div class="dynamic-list-inputs">
              <div v-for="(tip, idx) in formData.tips" :key="idx" class="dynamic-row">
                <input type="text" v-model="formData.tips[idx]" :disabled="isSubmitting || isLockedFromEdit" placeholder="Enter care tip..." class="dynamic-input">
                <button type="button" @click="removeTip(idx)" :disabled="isSubmitting || isLockedFromEdit" class="btn btn-xs btn-danger"><i class="fa-solid fa-xmark"></i></button>
              </div>
            </div>
          </div>
        </div>

        <!-- Form Action Buttons -->
        <div class="form-actions-bar">
          <button v-if="!isLockedFromEdit" type="submit" :disabled="isSubmitting" class="btn btn-primary btn-lg">
            <i class="fa-solid" :class="isSubmitting ? 'fa-circle-notch fa-spin' : 'fa-cloud-arrow-up'"></i>
            {{ isSubmitting ? 'Saving Record...' : (isEditMode ? 'Update Hairstyle Record' : 'Save Hairstyle Record') }}
          </button>
          <router-link to="/catalog" class="btn btn-light" :class="{'disabled-link': isSubmitting}">
            {{ isLockedFromEdit ? 'Back to Catalog' : 'Cancel' }}
          </router-link>
        </div>
      </template>

    </form>

    <!-- Saving Record Modal Popup -->
    <SavingModal 
      :show="isSubmitting"
      :is-edit-mode="isEditMode"
      :percentage="uploadProgress.percentage"
      :current-task="uploadProgress.currentTask"
    />
  </section>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { fetchFromFirestore, saveToFirestore, updateInFirestore, isFirestoreReady } from '../services/firebase.js';
import { uploadToCloudinaryDirect } from '../services/cloudinary.js';
import SavingModal from '../components/SavingModal.vue';

const emit = defineEmits(['notify', 'refresh-count']);
const route = useRoute();
const router = useRouter();

const isEditMode = computed(() => Boolean(route.params.id));
const isSubmitting = ref(false);
const isLoadingRecord = ref(false);
const isLockedFromEdit = ref(false);

const uploadProgress = reactive({
  percentage: 0,
  currentTask: "Preparing upload..."
});

const angleTypes = [
  { key: "main", label: "Main Cover / Thumbnail", icon: "fa-solid fa-star" },
  { key: "front", label: "Front View", icon: "fa-solid fa-user" },
  { key: "side", label: "Side View", icon: "fa-solid fa-user-ninja" },
  { key: "34", label: "3/4 Angle View", icon: "fa-solid fa-user-astronaut" },
  { key: "back", label: "Back View", icon: "fa-solid fa-circle-user" }
];

const faceShapeKeys = [
  { key: "oval", label: "Oval Face" },
  { key: "round", label: "Round Face" },
  { key: "square", label: "Square Face" },
  { key: "heart", label: "Heart Face" },
  { key: "diamond", label: "Diamond Face" },
  { key: "oblong", label: "Oblong Face" }
];

const formData = reactive({
  id: null,
  status: "draft",
  name: "",
  slug: "",
  variation_name: "",
  faceshape: "oval",
  gender: "male",
  tagline: "",
  shape_badge: "",
  score_badge: "",
  hair_length: "Short",
  hair_texture: "Straight / Soft Waves",
  styling_time: "",
  maintenance: "Easy",
  description: "",
  reasons: [""],
  tips: [""],
  scores: { oval: "", round: "", square: "", heart: "", diamond: "", oblong: "" }
});

const errors = reactive({ name: "", slug: "", faceshape: "", description: "" });
const userEditedSlug = ref(false);

const imageFiles = reactive({ main: null, front: null, side: null, 34: null, back: null });
const imageUrls = reactive({ main: "", front: "", side: "", 34: "", back: "" });
const previews = reactive({ main: "", front: "", side: "", 34: "", back: "" });

Object.keys(imageUrls).forEach(key => {
  watch(() => imageUrls[key], (newUrl) => {
    if (newUrl && !imageFiles[key]) {
      previews[key] = newUrl;
    }
  });
});

const onNameInput = () => {
  if (!isEditMode.value && !userEditedSlug.value) {
    formData.slug = formData.name.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');
  }
};

const loadRecordForEdit = async (id) => {
  isLoadingRecord.value = true;
  try {
    let record = null;
    if (isFirestoreReady()) {
      const items = await fetchFromFirestore();
      record = items.find(i => i.id === id);
    }

    if (record) {
      formData.id = record.id;
      formData.status = record.status || "draft";
      formData.name = record.name || "";
      formData.slug = record.slug || "";
      formData.variation_name = record.variation_name || "";
      formData.faceshape = record.faceshape || "oval";
      formData.gender = record.gender || "male";
      formData.tagline = record.tagline || "";
      formData.shape_badge = record.shape_badge || "";
      formData.score_badge = record.score_badge || "";
      formData.hair_length = record.hair_length || "Short";
      formData.hair_texture = record.hair_texture || "Straight / Soft Waves";
      formData.styling_time = record.styling_time || "";
      formData.maintenance = record.maintenance || "Easy";
      formData.description = record.description || "";
      formData.reasons = record.reasons && record.reasons.length ? [...record.reasons] : [""];
      formData.tips = record.tips && record.tips.length ? [...record.tips] : [""];

      if (formData.status === 'main_page') {
        isLockedFromEdit.value = true;
        emit("notify", { message: "🔒 Main Page record is locked from editing.", type: "info" });
      }

      userEditedSlug.value = true;

      imageUrls.main = record.main_img || ""; previews.main = record.main_img || "";
      const angles = record.angles || [];
      const front = angles.find(a => a.name === "Front") || {};
      const side = angles.find(a => a.name === "Side") || {};
      const three4 = angles.find(a => a.name === "3/4 View") || {};
      const back = angles.find(a => a.name === "Back") || {};

      imageUrls.front = front.img || ""; previews.front = front.img || "";
      imageUrls.side = side.img || ""; previews.side = side.img || "";
      imageUrls['34'] = three4.img || ""; previews['34'] = three4.img || "";
      imageUrls.back = back.img || ""; previews.back = back.img || "";

      const suit = record.suitability || [];
      faceShapeKeys.forEach(s => {
        const entry = suit.find(e => e.shape.toLowerCase().includes(s.key));
        formData.scores[s.key] = entry ? entry.score : "";
      });
    }
  } catch (err) {
    console.error("Error loading record:", err);
  } finally {
    isLoadingRecord.value = false;
  }
};

onMounted(() => {
  if (isEditMode.value) {
    loadRecordForEdit(route.params.id);
  }
});

const handleFileSelection = (file, key) => {
  if (!file || !file.type.startsWith("image/")) return;
  imageFiles[key] = file;
  const reader = new FileReader();
  reader.onload = (e) => previews[key] = e.target.result;
  reader.readAsDataURL(file);
};

const onSelectFile = (e, key) => {
  if (e.target.files && e.target.files[0]) handleFileSelection(e.target.files[0], key);
};

const onDropFile = (e, key) => {
  if (isSubmitting.value || isLockedFromEdit.value) return;
  const files = e.dataTransfer.files;
  if (files && files.length > 0) handleFileSelection(files[0], key);
};

const addReason = () => formData.reasons.push("");
const removeReason = (idx) => formData.reasons.splice(idx, 1);
const addTip = () => formData.tips.push("");
const removeTip = (idx) => formData.tips.splice(idx, 1);

const validateForm = () => {
  let isValid = true;
  errors.name = ""; errors.slug = ""; errors.faceshape = ""; errors.description = "";

  if (!formData.name.trim()) {
    errors.name = "Hairstyle name is required."; isValid = false;
  }
  if (!formData.slug.trim()) {
    errors.slug = "URL Slug is required."; isValid = false;
  } else if (!/^[a-z0-9_]+$/.test(formData.slug.trim())) {
    errors.slug = "Slug must contain only lowercase letters, numbers, and underscores."; isValid = false;
  }
  if (!formData.faceshape) {
    errors.faceshape = "Please select a face shape."; isValid = false;
  }
  if (!formData.description.trim()) {
    errors.description = "Full description is required."; isValid = false;
  }
  return isValid;
};

const handleSubmit = async () => {
  if (isLockedFromEdit.value) {
    emit("notify", { message: "Main Page records cannot be edited.", type: "error" });
    return;
  }

  if (!validateForm()) {
    emit("notify", { message: "Please fix form validation errors.", type: "error" });
    return;
  }

  isSubmitting.value = true;
  uploadProgress.percentage = 10;
  uploadProgress.currentTask = "Initializing Cloudinary upload...";

  try {
    const folder = `hairstyles/${formData.faceshape}/${formData.slug}`;
    const finalUrls = {};
    const keys = ['main', 'front', 'side', '34', 'back'];
    
    let processed = 0;
    for (const key of keys) {
      if (imageFiles[key]) {
        uploadProgress.currentTask = `Uploading ${key.toUpperCase()} angle photo to Cloudinary CDN...`;
        finalUrls[key] = await uploadToCloudinaryDirect(imageFiles[key], folder);
      } else {
        finalUrls[key] = imageUrls[key] || "";
      }

      if (finalUrls[key] && finalUrls[key].startsWith('data:image/')) {
        throw new Error(`Image '${key}' must be uploaded to Cloudinary CDN. Base64 data is not allowed in Firebase.`);
      }

      processed++;
      uploadProgress.percentage = 10 + Math.round((processed / keys.length) * 70);
    }

    uploadProgress.currentTask = "Saving record metadata to Firebase Firestore...";
    uploadProgress.percentage = 90;

    const record = {
      status: formData.status,
      name: formData.name.trim(),
      slug: formData.slug.trim(),
      variation_name: formData.variation_name.trim() || formData.name.trim(),
      faceshape: formData.faceshape,
      ideal_shape: formData.faceshape,
      gender: formData.gender,
      tagline: formData.tagline.trim(),
      shape_badge: formData.shape_badge.trim(),
      score_badge: formData.score_badge.trim(),
      hair_length: formData.hair_length,
      hair_texture: formData.hair_texture,
      styling_time: formData.styling_time.trim(),
      maintenance: formData.maintenance,
      main_img: finalUrls.main || finalUrls.front || "",
      description: formData.description.trim(),
      reasons: formData.reasons.map(r => r.trim()).filter(r => r.length > 0),
      tips: formData.tips.map(t => t.trim()).filter(t => t.length > 0),
      suitability: faceShapeKeys.map(s => ({
        shape: s.label,
        score: formData.scores[s.key] ? formData.scores[s.key].trim() : ""
      })),
      angles: [
        { name: "Front", img: finalUrls.front || finalUrls.main || "" },
        { name: "Side", img: finalUrls.side || "" },
        { name: "3/4 View", img: finalUrls['34'] || "" },
        { name: "Back", img: finalUrls.back || "" }
      ]
    };

    if (isEditMode.value) {
      if (isFirestoreReady()) {
        await updateInFirestore(formData.id, record);
      }
      uploadProgress.percentage = 100;
      uploadProgress.currentTask = "Record updated successfully!";
      emit("notify", { message: `Hairstyle '${record.name}' updated!`, type: "success" });
    } else {
      record.created_at = new Date().toISOString();
      if (isFirestoreReady()) {
        await saveToFirestore(record);
      }
      uploadProgress.percentage = 100;
      uploadProgress.currentTask = "Record saved successfully!";
      emit("notify", { message: `Hairstyle '${record.name}' created!`, type: "success" });
    }

    setTimeout(() => {
      isSubmitting.value = false;
      router.push("/catalog");
    }, 600);

  } catch (err) {
    console.error("Submit Error:", err);
    emit("notify", { message: err.message, type: "error" });
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.form-pane {
  animation: fadeIn 0.3s ease;
}

.form-disabled {
  opacity: 0.65;
  pointer-events: none;
}

/* Locked Banner */
.locked-banner {
  background: #fef2f2;
  border: 1px solid #fca5a5;
  border-radius: 16px;
  padding: 1.2rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  color: #991b1b;
}

.lock-banner-icon {
  font-size: 2rem;
  color: #dc2626;
}

.locked-banner h3 {
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.locked-banner p {
  font-size: 0.88rem;
}

.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  color: #64748b;
  margin-bottom: 1.5rem;
}

.spinner-icon {
  font-size: 2.5rem;
  color: #7C3AED;
  margin-bottom: 1rem;
}

.form-card {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  padding: 1.75rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 10px 30px -5px rgba(124, 58, 237, 0.05);
}

.card-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1E1B4B;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f1f5f9;
  width: 100%;
}

.card-title i { color: #7C3AED; }

.section-desc {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 1.25rem;
}

.form-grid {
  display: grid;
  gap: 1.25rem;
}

.form-grid.col-3 { grid-template-columns: repeat(3, 1fr); }
.form-grid.col-4 { grid-template-columns: repeat(4, 1fr); }

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group.margin-bottom { margin-bottom: 1.25rem; }

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1E1B4B;
}

.required { color: #EC4899; }

.form-group.has-error input,
.form-group.has-error select,
.form-group.has-error textarea {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
}

.error-msg {
  font-size: 0.78rem;
  color: #ef4444;
  font-weight: 600;
  margin-top: 0.2rem;
}

/* Custom Select Controls */
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
  transition: transform 0.2s ease;
}

.custom-select {
  appearance: none;
  width: 100%;
  padding: 0.65rem 2.2rem 0.65rem 2.4rem;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  font-size: 0.88rem;
  background: #ffffff;
  font-weight: 600;
  color: #1E1B4B;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.custom-select:hover {
  border-color: #7C3AED;
  background: #FAF8FF;
}

.custom-select:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15);
}

input[type="text"], textarea {
  font-family: inherit;
  font-size: 0.9rem;
  padding: 0.65rem 0.85rem;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  background: #fff;
  color: #1E1B4B;
  transition: all 0.2s ease;
}

input[type="text"]:focus, textarea:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15);
}

.upload-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
}

.upload-box {
  background: #FAF8FF;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.upload-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #1E1B4B;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.upload-label i { color: #7C3AED; }

.dropzone {
  position: relative;
  height: 160px;
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  cursor: pointer;
  overflow: hidden;
}

.dropzone.is-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.dropzone input[type="file"] {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 10;
}

.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  color: #64748b;
  font-size: 0.75rem;
}

.img-preview {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  object-fit: cover;
  display: none;
  z-index: 5;
}

.img-preview.has-image { display: block; }

.url-override {
  font-size: 0.78rem;
  padding: 0.4rem 0.6rem;
}

.dynamic-list-inputs {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.dynamic-row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.dynamic-row input { flex: 1; }

.score-input-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FAF8FF;
  border: 1px solid #e2e8f0;
  padding: 0.45rem 0.75rem;
  border-radius: 10px;
  font-size: 0.85rem;
}

.score-input-group span { font-weight: 600; color: #1E1B4B; }
.score-input-group input { width: 110px; text-align: right; }

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
  transition: all 0.2s ease;
}

.disabled-link {
  opacity: 0.5;
  pointer-events: none;
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

.btn-secondary { background: #1E1B4B; color: #fff; }
.btn-light { background: #fff; border-color: #cbd5e1; color: #1E1B4B; }
.btn-danger { background: #ef4444; color: #fff; }
.btn-xs { padding: 0.25rem 0.6rem; font-size: 0.75rem; border-radius: 6px; }
.btn-lg { padding: 0.85rem 2rem; font-size: 1rem; }

.form-actions-bar {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.label-with-btn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.4rem;
}
</style>
