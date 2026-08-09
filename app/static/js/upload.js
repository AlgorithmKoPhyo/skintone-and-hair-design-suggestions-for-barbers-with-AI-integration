/* ==========================================================================
   StyleMe - File Upload Controller (Drag & Drop + Gender Modal Flow)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initFileUpload();
});

function initFileUpload() {
  const fileInput = document.getElementById('file-upload-input');
  const btnUpload = document.getElementById('btn-upload-image');
  const uploadCard = document.getElementById('upload-action-card');
  const genderModal = document.getElementById('modal-gender-select');
  const btnOptFemale = document.getElementById('gender-opt-female');
  const btnOptMale = document.getElementById('gender-opt-male');

  let pendingFile = null;

  // File Input Click Trigger
  if (btnUpload && fileInput) {
    btnUpload.addEventListener('click', (e) => {
      e.stopPropagation();
      fileInput.click();
    });
  }

  if (uploadCard && fileInput) {
    uploadCard.addEventListener('click', (e) => {
      if (e.target !== btnUpload && !btnUpload.contains(e.target)) {
        fileInput.click();
      }
    });

    // ----------------------------------------------------------------------
    // Drag & Drop Event Listeners
    // ----------------------------------------------------------------------
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      uploadCard.addEventListener(eventName, preventDefaults, false);
      document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      uploadCard.addEventListener(eventName, () => {
        uploadCard.classList.add('drag-over');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      uploadCard.addEventListener(eventName, () => {
        uploadCard.classList.remove('drag-over');
      }, false);
    });

    uploadCard.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;

      if (files && files.length > 0) {
        const file = files[0];
        if (file.type.startsWith('image/')) {
          handleSelectedFile(file);
        } else {
          alert('Please drop an image file (JPEG, PNG, WEBP).');
        }
      }
    }, false);

    fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleSelectedFile(e.target.files[0]);
      }
    });
  }

  function handleSelectedFile(file) {
    pendingFile = file;
    if (genderModal) {
      genderModal.classList.add('active');
    } else {
      submitUploadFile(pendingFile, 'female');
    }
  }

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  // Handle Gender modal selections
  if (btnOptFemale) {
    btnOptFemale.addEventListener('click', () => {
      if (genderModal) genderModal.classList.remove('active');
      if (pendingFile) submitUploadFile(pendingFile, 'female');
    });
  }

  if (btnOptMale) {
    btnOptMale.addEventListener('click', () => {
      if (genderModal) genderModal.classList.remove('active');
      if (pendingFile) submitUploadFile(pendingFile, 'male');
    });
  }

  // Close gender modal when clicking outside
  if (genderModal) {
    genderModal.addEventListener('click', (e) => {
      if (e.target === genderModal) {
        genderModal.classList.remove('active');
      }
    });
  }
}

async function submitUploadFile(file, gender) {
  const btnUpload = document.getElementById('btn-upload-image');
  if (btnUpload) {
    btnUpload.disabled = true;
    btnUpload.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
  }

  const formData = new FormData();
  formData.append('image', file);
  formData.append('gender', gender);
  formData.append('analysis_type', 'hairstyle');

  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    if (data.redirect_url) {
      window.location.href = data.redirect_url;
    } else {
      window.location.href = `/recommendation?gender=${gender}`;
    }
  } catch (err) {
    console.error("Analysis upload error:", err);
    window.location.href = `/recommendation?gender=${gender}`;
  }
}
