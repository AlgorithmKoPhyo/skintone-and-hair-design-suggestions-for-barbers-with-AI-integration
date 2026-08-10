/* ==========================================================================
   StyleMe - Global Gender Selection Upload Controller (Improved)
   - Fixes double-listener conflict with recommendation.js
   - File size validation (max 10 MB)
   - Photo thumbnail preview inside modal
   - Loading spinner overlay after gender chosen
   ========================================================================== */

(function () {
  'use strict';

  const MAX_FILE_MB = 10;
  const MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024;

  // ---- State ---------------------------------------------------------------
  let pendingFile = null;

  // ---- DOM helpers ---------------------------------------------------------
  const $ = (id) => document.getElementById(id);

  function getModal() { return $('modal-gender-select'); }
  function getBtnFemale() { return $('gender-opt-female'); }
  function getBtnMale() { return $('gender-opt-male'); }

  // ---- File size check -----------------------------------------------------
  function validateFile(file) {
    if (!file.type.startsWith('image/')) {
      StyleMe.toast('Please select an image file (JPEG, PNG, WEBP).', 'error');
      return false;
    }
    if (file.size > MAX_FILE_BYTES) {
      StyleMe.toast(
        `Photo is too large (${(file.size / 1024 / 1024).toFixed(1)} MB). Max allowed: ${MAX_FILE_MB} MB.`,
        'error'
      );
      return false;
    }
    return true;
  }

  // ---- Image preview inside modal ------------------------------------------
  function updateModalPreview(file) {
    const previewBar = $('gender-modal-preview-bar');
    const thumb = $('gender-modal-thumb');
    const nameEl = $('gender-modal-filename');
    const sizeEl = $('gender-modal-filesize');

    if (!previewBar || !thumb) return;

    const sizeMB = (file.size / 1024 / 1024).toFixed(2);
    if (nameEl) nameEl.textContent = file.name;
    if (sizeEl) sizeEl.textContent = `${sizeMB} MB · ${file.type.split('/')[1].toUpperCase()}`;

    const reader = new FileReader();
    reader.onload = (e) => {
      thumb.src = e.target.result;
      previewBar.style.display = 'flex';
    };
    reader.readAsDataURL(file);
  }

  function resetModalPreview() {
    const previewBar = $('gender-modal-preview-bar');
    const thumb = $('gender-modal-thumb');
    if (previewBar) previewBar.style.display = 'none';
    if (thumb) thumb.src = '';
  }

  // ---- Loading overlay (post-selection analysis) -------------------------
  function showLoading() {
    const el = $('gender-modal-loading');
    if (el) el.style.display = 'flex';

    // Disable both gender buttons
    const btnF = getBtnFemale();
    const btnM = getBtnMale();
    if (btnF) btnF.disabled = true;
    if (btnM) btnM.disabled = true;
  }

  // ---- Face validation UI state -------------------------------------------
  //  state: 'scanning' | 'valid' | 'invalid'
  function setValidationState(state, message) {
    const scanStatus = $('face-scan-status');
    const warning = $('face-validation-warning');
    const msgEl = $('face-validation-msg');
    const btnF = getBtnFemale();
    const btnM = getBtnMale();
    const btnC = $('opt-color-analysis');
    const subtitle = $('gender-modal-subtitle');
    const statusIcon = $('gender-modal-status-icon');

    // Hide both indicators first
    if (scanStatus) scanStatus.style.display = 'none';
    if (warning) warning.style.display = 'none';

    if (state === 'scanning') {
      // Buttons disabled, spinner shown — reset icon to neutral green while waiting
      if (statusIcon) {
        statusIcon.className = 'fa-solid fa-circle-check';
        statusIcon.style.color = '#22C55E';
      }
      if (scanStatus) scanStatus.style.display = 'flex';
      if (btnF) btnF.disabled = true;
      if (btnM) btnM.disabled = true;
      if (btnC) btnC.disabled = true;
      if (subtitle) subtitle.textContent = 'Which recommendation would you like our AI to generate?';

    } else if (state === 'valid') {
      // Face found — green check, enable buttons
      if (statusIcon) {
        statusIcon.className = 'fa-solid fa-circle-check';
        statusIcon.style.color = '#22C55E';
      }
      if (btnF) btnF.disabled = false;
      if (btnM) btnM.disabled = false;
      if (btnC) {
        btnC.disabled = false;
        btnC.style.display = 'flex';
      }
      if (subtitle) subtitle.textContent = 'Which recommendation would you like our AI to generate?';

    } else if (state === 'invalid') {
      // No face — red cross, keep buttons disabled, show warning
      if (statusIcon) {
        statusIcon.className = 'fa-solid fa-circle-xmark';
        statusIcon.style.color = '#EF4444';
      }
      if (warning) warning.style.display = 'flex';
      if (msgEl && message) msgEl.textContent = message;
      if (btnF) btnF.disabled = true;
      if (btnM) btnM.disabled = true;
      if (btnC) btnC.disabled = true;
      if (subtitle) subtitle.textContent = 'Please upload a clear photo showing your face to continue.';
    }
  }

  // ---- Background face validation -----------------------------------------
  async function validateFaceInBackground(file) {
    setValidationState('scanning');
    try {
      const formData = new FormData();
      formData.append('image', file);
      const res = await fetch('/validate-face', { method: 'POST', body: formData });
      const data = await res.json();
      if (data.valid) {
        setValidationState('valid');
      } else {
        setValidationState('invalid', data.message || 'No face detected. Please upload a clear photo showing your face.');
      }
    } catch (err) {
      // Network/server error — fail open so the user isn't permanently blocked
      console.warn('[StyleMe] /validate-face failed, failing open:', err);
      setValidationState('valid');
    }
  }

  // ---- Modal open / close --------------------------------------------------
  function showGenderModal(file, _unused) {
    if (!validateFile(file)) return;
    pendingFile = file;
    updateModalPreview(file);

    // Reset loading overlay from previous use
    const loading = $('gender-modal-loading');
    if (loading) loading.style.display = 'none';

    // Reset validation warning/scan from previous use
    const scanStatus = $('face-scan-status');
    const warning = $('face-validation-warning');
    if (scanStatus) scanStatus.style.display = 'none';
    if (warning) warning.style.display = 'none';

    const modalTitle = $('gender-modal-title');
    if (modalTitle) modalTitle.textContent = 'Select Recommendation';
    const modalSubtitle = $('gender-modal-subtitle');
    if (modalSubtitle) modalSubtitle.textContent = 'Which recommendation would you like our AI to generate?';

    // Open the modal immediately for good UX
    const modal = getModal();
    if (modal) modal.classList.add('active');

    // Kick off background face validation (disables buttons until result)
    validateFaceInBackground(file);
  }

  function closeModal() {
    const modal = getModal();
    if (modal) modal.classList.remove('active');
    resetModalPreview();
    pendingFile = null;
  }

  // ---- Submit to API -------------------------------------------------------
  async function submitToAPI(file, gender, analysisType = 'hairstyle') {
    showLoading();

    const formData = new FormData();
    if (analysisType === 'color') {
      formData.append('file', file, 'photo.jpg');
    } else {
      formData.append('image', file);
    }
    formData.append('gender', gender);
    formData.append('analysis_type', analysisType);

    try {
      if (analysisType === 'color') {
        const res = await fetch('/analyze', { method: 'POST', body: formData });
        if (!res.ok) throw new Error('Network response was not ok');
        const html = await res.text();
        document.open();
        document.write(html);
        document.close();
      } else {
        const res = await fetch('/api/analyze', { method: 'POST', body: formData });
        const data = await res.json();
        window.location.href = data.redirect_url || `/recommendation?gender=${gender}`;
      }
    } catch {
      window.location.href = `/recommendation?gender=${gender}`;
    }
  }

  // ---- Wire gender buttons (idempotent) ------------------------------------
  function wireGenderButtons() {
    const btnF = getBtnFemale();
    const btnM = getBtnMale();
    const btnC = $('opt-color-analysis');

    if (btnF && !btnF._genderBound) {
      btnF._genderBound = true;
      btnF.addEventListener('click', () => {
        if (!pendingFile) return;
        submitToAPI(pendingFile, 'female', 'hairstyle');
      });
    }

    if (btnM && !btnM._genderBound) {
      btnM._genderBound = true;
      btnM.addEventListener('click', () => {
        if (!pendingFile) return;
        submitToAPI(pendingFile, 'male', 'hairstyle');
      });
    }

    if (btnC && !btnC._colorBound) {
      btnC._colorBound = true;
      btnC.addEventListener('click', () => {
        if (!pendingFile) return;
        submitToAPI(pendingFile, 'female', 'color');
      });
    }

    // Cancel button
    const cancelBtn = $('gender-modal-cancel');
    if (cancelBtn && !cancelBtn._cancelBound) {
      cancelBtn._cancelBound = true;
      cancelBtn.addEventListener('click', closeModal);
    }

    // Close on backdrop click
    const modal = getModal();
    if (modal && !modal._backdropBound) {
      modal._backdropBound = true;
      modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
      });
    }
  }

  // ---- Patch <input type="file"> -------------------------------------------
  function patchFileInput(input) {
    if (input._genderPatched) return;
    input._genderPatched = true;

    input.addEventListener('change', (e) => {
      const file = e.target.files && e.target.files[0];
      input.value = ''; // allow re-selecting same file
      if (file) showGenderModal(file);
    });
  }

  // ---- Patch drag-and-drop zone --------------------------------------------
  function patchDropZone(zone) {
    if (zone._genderDropPatched) return;
    zone._genderDropPatched = true;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(ev =>
      zone.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); })
    );
    ['dragenter', 'dragover'].forEach(ev =>
      zone.addEventListener(ev, () => zone.classList.add('drag-over'))
    );
    ['dragleave', 'drop'].forEach(ev =>
      zone.addEventListener(ev, () => zone.classList.remove('drag-over'))
    );

    zone.addEventListener('drop', (e) => {
      const file = e.dataTransfer.files && e.dataTransfer.files[0];
      if (file) showGenderModal(file);
    });
  }

  // ---- Main init -----------------------------------------------------------
  function init() {
    wireGenderButtons();

    // Home page
    const uploadCard = $('upload-action-card');
    const fileInput = $('file-upload-input');
    const btnUpload = $('btn-upload-image');

    if (fileInput) patchFileInput(fileInput);
    if (uploadCard) patchDropZone(uploadCard);
    if (btnUpload && fileInput && !btnUpload._clickBound) {
      btnUpload._clickBound = true;
      btnUpload.addEventListener('click', (e) => { e.stopPropagation(); fileInput.click(); });
    }

    // Recommendation page
    const quickInput = $('rec-quick-file-input');
    const heroDropZone = $('rec-drag-drop-zone');
    const noPhotoZone = $('no-photo-dropzone');

    if (quickInput) patchFileInput(quickInput);
    if (heroDropZone) patchDropZone(heroDropZone);
    if (noPhotoZone) patchDropZone(noPhotoZone);

    [$('btn-quick-upload'), $('btn-modal-upload'), $('btn-modal-change-photo')].forEach(btn => {
      if (btn && !btn._triggerBound) {
        btn._triggerBound = true;
        btn.addEventListener('click', () => quickInput && quickInput.click());
      }
    });
  }

  // DOM ready guard
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Public API (camera.js and other scripts can call this)
  window.StyleMeGender = { showGenderModal, closeModal, submitToAPI };
})();
