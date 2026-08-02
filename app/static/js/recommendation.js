/* ==========================================================================
   StyleMe - Hairstyle Recommendation Controller (Drag & Drop + Dynamic API)
   ========================================================================== */

let activeGender = 'female';
let activeShape = 'oval';

document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const genderParam = urlParams.get('gender');
  const shapeParam = urlParams.get('shape');

  if (genderParam === 'male') {
    activeGender = 'male';
  } else {
    activeGender = 'female';
  }

  if (shapeParam && ['oval', 'round', 'square', 'heart'].includes(shapeParam)) {
    activeShape = shapeParam;
  }

  // Use server-rendered database record if available, or fetch via REST API
  if (window.SERVER_REC_DATA) {
    updateRecommendationViewFromDB(window.SERVER_REC_DATA, window.SERVER_RELATED_STYLES);
  } else {
    fetchRecommendationFromAPI(activeGender, activeShape);
  }

  initAngleSwitcher();
  initHairstyleGallery();
  initFaceShapeModal();
  initQuickPhotoUpload();
});

async function fetchRecommendationFromAPI(gender, shape) {
  try {
    const res = await fetch(`/api/recommendation?gender=${gender}&shape=${shape}`);
    const json = await res.json();
    if (json.status === 'success' && json.data) {
      updateRecommendationViewFromDB(json.data, json.related_styles);
    }
  } catch (err) {
    console.error("Error fetching recommendation from database API:", err);
  }
}

function initAngleSwitcher() {
  const angleCards = document.querySelectorAll('.angle-card');
  const mainPreviewImg = document.getElementById('main-ai-preview-img');

  angleCards.forEach(card => {
    card.addEventListener('click', () => {
      angleCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');

      const targetSrc = card.getAttribute('data-img');
      if (mainPreviewImg && targetSrc) {
        mainPreviewImg.style.opacity = '0.3';
        setTimeout(() => {
          mainPreviewImg.src = targetSrc;
          mainPreviewImg.style.opacity = '1';
        }, 150);
      }
    });
  });
}

function initHairstyleGallery() {
  const galleryCards = document.querySelectorAll('.style-variation-card');
  const mainPreviewImg = document.getElementById('main-ai-preview-img');
  const titleElem = document.getElementById('rec-style-title');

  galleryCards.forEach(card => {
    card.addEventListener('click', () => {
      galleryCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');

      const styleTitle = card.getAttribute('data-title');
      const styleImg = card.getAttribute('data-img');

      if (titleElem && styleTitle) titleElem.textContent = styleTitle;
      if (mainPreviewImg && styleImg) {
        mainPreviewImg.style.opacity = '0.3';
        setTimeout(() => {
          mainPreviewImg.src = styleImg;
          mainPreviewImg.style.opacity = '1';
        }, 150);
      }

      const recCard = document.querySelector('.main-rec-card');
      if (recCard) {
        recCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });
}

function initFaceShapeModal() {
  const badgeBtn = document.getElementById('face-shape-badge-btn');
  const modalBackdrop = document.getElementById('modal-face-shapes');
  const closeModalBtn = document.getElementById('btn-close-modal');

  if (badgeBtn && modalBackdrop) {
    badgeBtn.addEventListener('click', () => {
      modalBackdrop.classList.add('active');
    });
  }

  if (closeModalBtn && modalBackdrop) {
    closeModalBtn.addEventListener('click', () => {
      modalBackdrop.classList.remove('active');
    });
  }

  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) {
        modalBackdrop.classList.remove('active');
      }
    });
  }
}

function initQuickPhotoUpload() {
  const quickFileInput = document.getElementById('rec-quick-file-input');
  const btnQuickUpload = document.getElementById('btn-quick-upload');
  const btnModalUpload = document.getElementById('btn-modal-upload');
  const btnModalChange = document.getElementById('btn-modal-change-photo');
  const heroDropZone = document.getElementById('rec-drag-drop-zone');
  const noPhotoDropZone = document.getElementById('no-photo-dropzone');
  const modalImageContainer = document.getElementById('modal-analyzed-img')?.parentElement;
  const genderModal = document.getElementById('modal-gender-select');
  const btnOptFemale = document.getElementById('gender-opt-female');
  const btnOptMale = document.getElementById('gender-opt-male');

  let pendingFile = null;

  const triggerFileSelect = () => {
    if (quickFileInput) quickFileInput.click();
  };

  if (btnQuickUpload) btnQuickUpload.addEventListener('click', triggerFileSelect);
  if (btnModalUpload) btnModalUpload.addEventListener('click', triggerFileSelect);
  if (btnModalChange) btnModalChange.addEventListener('click', triggerFileSelect);

  // Add Drag & Drop to Hero Preview Card (#rec-drag-drop-zone)
  if (heroDropZone) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      heroDropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
      }, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      heroDropZone.addEventListener(eventName, () => {
        heroDropZone.classList.add('drag-over');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      heroDropZone.addEventListener(eventName, () => {
        heroDropZone.classList.remove('drag-over');
      }, false);
    });

    heroDropZone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0 && files[0].type.startsWith('image/')) {
        pendingFile = files[0];
        if (genderModal) {
          genderModal.classList.add('active');
        } else {
          submitQuickUploadFile(pendingFile, activeGender);
        }
      }
    });
  }

  // Add Drag & Drop to NO PHOTO STATE Container (#no-photo-dropzone)
  if (noPhotoDropZone) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      noPhotoDropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
      }, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      noPhotoDropZone.addEventListener(eventName, () => {
        noPhotoDropZone.style.border = '2px dashed var(--purple-primary)';
        noPhotoDropZone.style.background = 'var(--purple-light)';
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      noPhotoDropZone.addEventListener(eventName, () => {
        noPhotoDropZone.style.border = '1px solid var(--border-light)';
        noPhotoDropZone.style.background = 'var(--bg-card)';
      }, false);
    });

    noPhotoDropZone.addEventListener('click', (e) => {
      if (e.target !== btnQuickUpload && !btnQuickUpload.contains(e.target) && !e.target.closest('a')) {
        triggerFileSelect();
      }
    });

    noPhotoDropZone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0 && files[0].type.startsWith('image/')) {
        pendingFile = files[0];
        if (genderModal) {
          genderModal.classList.add('active');
        } else {
          submitQuickUploadFile(pendingFile, activeGender);
        }
      }
    });
  }

  // Add Drag & Drop to Modal Analyzed Image Container
  if (modalImageContainer) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      modalImageContainer.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
      }, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      modalImageContainer.addEventListener(eventName, () => {
        modalImageContainer.style.border = '2px dashed var(--purple-primary)';
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      modalImageContainer.addEventListener(eventName, () => {
        modalImageContainer.style.border = '1px solid var(--border-light)';
      }, false);
    });

    modalImageContainer.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0 && files[0].type.startsWith('image/')) {
        pendingFile = files[0];
        if (genderModal) {
          genderModal.classList.add('active');
        } else {
          submitQuickUploadFile(pendingFile, activeGender);
        }
      }
    });
  }

  if (quickFileInput) {
    quickFileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        pendingFile = e.target.files[0];
        if (genderModal) {
          genderModal.classList.add('active');
        } else {
          submitQuickUploadFile(pendingFile, activeGender);
        }
      }
    });
  }

  if (btnOptFemale) {
    btnOptFemale.addEventListener('click', () => {
      if (genderModal) genderModal.classList.remove('active');
      if (pendingFile) submitQuickUploadFile(pendingFile, 'female');
    });
  }

  if (btnOptMale) {
    btnOptMale.addEventListener('click', () => {
      if (genderModal) genderModal.classList.remove('active');
      if (pendingFile) submitQuickUploadFile(pendingFile, 'male');
    });
  }
}

async function submitQuickUploadFile(file, gender) {
  const btnQuickUpload = document.getElementById('btn-quick-upload');
  const btnModalUpload = document.getElementById('btn-modal-upload');

  if (btnQuickUpload) {
    btnQuickUpload.disabled = true;
    btnQuickUpload.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
  }
  if (btnModalUpload) {
    btnModalUpload.disabled = true;
    btnModalUpload.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
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
      window.location.reload();
    }
  } catch (err) {
    console.error("Quick photo upload error:", err);
    window.location.reload();
  }
}

function updateRecommendationViewFromDB(data, relatedStyles = []) {
  const titleElem = document.getElementById('rec-style-title');
  const taglineElem = document.getElementById('rec-style-tagline');
  const descElem = document.getElementById('rec-style-desc');
  const mainImg = document.getElementById('main-ai-preview-img');
  const checklistContainer = document.getElementById('rec-checklist');
  const detailLength = document.getElementById('detail-length');
  const detailTexture = document.getElementById('detail-texture');
  const detailMaint = document.getElementById('detail-maintenance');
  const detailScore = document.getElementById('detail-score');
  const tipsListContainer = document.getElementById('rec-tips-list');
  const galleryContainer = document.getElementById('more-styles-cards-container');

  if (titleElem && data.name) titleElem.textContent = data.name;
  if (taglineElem && data.tagline) taglineElem.textContent = data.tagline;
  if (descElem && data.description) descElem.textContent = data.description;

  if (mainImg && data.main_img) {
    mainImg.style.opacity = '0.3';
    setTimeout(() => {
      mainImg.src = data.main_img;
      mainImg.style.opacity = '1';
    }, 150);
  }

  if (checklistContainer && data.reasons && data.reasons.length) {
    checklistContainer.innerHTML = data.reasons.map(r => `
      <li>
        <span class="check-icon"><i class="fa-solid fa-check"></i></span>
        <span>${r}</span>
      </li>
    `).join('');
  }

  if (detailLength && data.hair_length) detailLength.textContent = data.hair_length;
  if (detailTexture && data.hair_texture) detailTexture.textContent = data.hair_texture;
  if (detailMaint && data.maintenance) detailMaint.textContent = data.maintenance;
  if (detailScore && data.score_badge) detailScore.innerHTML = `★★★★★ ${data.score_badge}`;

  if (tipsListContainer && data.tips && data.tips.length) {
    tipsListContainer.innerHTML = data.tips.map(t => `<li>${t}</li>`).join('');
  }

  if (galleryContainer && relatedStyles && relatedStyles.length) {
    galleryContainer.innerHTML = relatedStyles.map((style, idx) => `
      <a href="/hairstyle-detail?style=${style.slug}&gender=${style.gender}" class="style-variation-card col-2 col-md-4 col-sm-6 ${idx === 0 ? 'active' : ''}" data-title="${style.name}" data-img="${style.main_img}" style="text-decoration: none; color: inherit;">
        <div class="var-img-wrapper">
          <img src="${style.main_img}" alt="${style.name}">
        </div>
        <div class="var-info">
          <div>
            <div class="var-title">${style.name}</div>
            <div class="var-sub">${style.hair_length}</div>
          </div>
          <div class="arrow-circle-btn">
            <i class="fa-solid fa-chevron-right"></i>
          </div>
        </div>
      </a>
    `).join('');
    initHairstyleGallery();
  }
}
