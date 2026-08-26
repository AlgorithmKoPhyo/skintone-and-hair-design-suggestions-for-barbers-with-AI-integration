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
    console.log("THis is the result", res)
    const json = await res.json();
    if (json.status === 'success' && json.data) {
      updateRecommendationViewFromDB(json.data, json.related_styles);
    }
  } catch (err) {
    console.error("Error fetching recommendation from database API:", err);
  }
}

function initAngleSwitcher() {
  const mainPreviewImg = document.getElementById('main-ai-preview-img');
  const btnPrev        = document.getElementById('rec-slider-prev');
  const btnNext        = document.getElementById('rec-slider-next');
  const labelEl        = document.getElementById('rec-slider-label');
  const dotsContainer  = document.getElementById('rec-slider-dots');
  const angleCards     = Array.from(document.querySelectorAll('.angle-card'));

  if (!mainPreviewImg || angleCards.length === 0) return;

  let currentIndex = 0;

  // Build pagination dots dynamically based on number of angles
  if (dotsContainer) {
    dotsContainer.innerHTML = '';
    angleCards.forEach((_, idx) => {
      const dot = document.createElement('div');
      dot.className = `slider-dot ${idx === 0 ? 'active' : ''}`;
      dot.setAttribute('data-idx', idx);
      dot.addEventListener('click', (e) => {
        e.stopPropagation();
        goToIndex(idx);
      });
      dotsContainer.appendChild(dot);
    });
  }

  function goToIndex(idx) {
    if (idx < 0) idx = angleCards.length - 1;
    if (idx >= angleCards.length) idx = 0;
    currentIndex = idx;

    const activeCard = angleCards[currentIndex];
    const targetSrc  = activeCard.getAttribute('data-img');
    const angleName  = activeCard.querySelector('.angle-name')?.textContent || `Angle ${currentIndex + 1}`;

    // Update active state of thumbnail cards
    angleCards.forEach((c, i) => {
      if (i === currentIndex) c.classList.add('active');
      else c.classList.remove('active');
    });

    // Update pagination dots
    if (dotsContainer) {
      const dots = dotsContainer.querySelectorAll('.slider-dot');
      dots.forEach((d, i) => {
        if (i === currentIndex) d.classList.add('active');
        else d.classList.remove('active');
      });
    }

    // Update label text
    if (labelEl) labelEl.textContent = angleName;

    // Smooth image transition
    if (mainPreviewImg && targetSrc && mainPreviewImg.src !== targetSrc) {
      mainPreviewImg.style.opacity = '0.2';
      setTimeout(() => {
        mainPreviewImg.src = targetSrc;
        mainPreviewImg.style.opacity = '1';
      }, 140);
    }
  }

  // Next / Prev button click listeners
  // Use onclick to overwrite existing listeners from previous initializations
  if (btnPrev) {
    btnPrev.onclick = (e) => {
      e.stopPropagation();
      goToIndex(currentIndex - 1);
    };
  }

  if (btnNext) {
    btnNext.onclick = (e) => {
      e.stopPropagation();
      goToIndex(currentIndex + 1);
    };
  }

  // Click on thumbnail card
  angleCards.forEach((card, idx) => {
    card.onclick = () => goToIndex(idx);
  });

  // Touch Swipe Gesture & Auto-play Support
  const wrapper = mainPreviewImg.closest('.rec-preview-wrapper');

  function startAutoPlay() {
    stopAutoPlay();
    window.recAutoTimer = setInterval(() => {
      goToIndex(currentIndex + 1);
    }, 4000);
  }

  function stopAutoPlay() {
    if (window.recAutoTimer) {
      clearInterval(window.recAutoTimer);
      window.recAutoTimer = null;
    }
  }

  startAutoPlay();

  if (wrapper) {
    wrapper.onmouseenter = stopAutoPlay;
    wrapper.onmouseleave = startAutoPlay;

    let touchStartX = 0;
    let touchEndX = 0;

    wrapper.ontouchstart = (e) => {
      stopAutoPlay();
      touchStartX = e.changedTouches[0].screenX;
    };

    wrapper.ontouchend = (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
      startAutoPlay();
    };

    function handleSwipe() {
      const diff = touchEndX - touchStartX;
      if (Math.abs(diff) > 40) {
        if (diff < 0) goToIndex(currentIndex + 1); // Swipe left → Next
        else goToIndex(currentIndex - 1);          // Swipe right → Prev
      }
    }
  }
}

function initHairstyleGallery() {
  const galleryCards = document.querySelectorAll('.style-variation-card');
  const mainPreviewImg = document.getElementById('main-ai-preview-img');
  const titleElem = document.getElementById('rec-style-title');

  galleryCards.forEach(card => {
    card.addEventListener('click', (e) => {
      e.preventDefault();
      
      const slug = card.getAttribute('data-slug');
      if (slug && window.SERVER_RELATED_STYLES) {
        const styleData = window.SERVER_RELATED_STYLES.find(s => s.slug === slug);
        if (styleData) {
          // Update the main view without re-rendering the gallery itself
          updateRecommendationViewFromDB(styleData, null);
        }
      }

      galleryCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');

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

  // Add Drag & Drop to Upload Card (#btn-quick-upload)
  if (btnQuickUpload) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      btnQuickUpload.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
      }, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      btnQuickUpload.addEventListener(eventName, () => {
        btnQuickUpload.classList.add('drag-over');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      btnQuickUpload.addEventListener(eventName, () => {
        btnQuickUpload.classList.remove('drag-over');
      }, false);
    });

    btnQuickUpload.addEventListener('drop', (e) => {
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
  const anglesGrid = document.querySelector('.angles-thumbnails-grid');

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
  
  if (anglesGrid) {
    if (data.angles && data.angles.length > 0) {
      anglesGrid.innerHTML = data.angles.map((angle, idx) => `
        <div class="angle-card col-3 col-sm-6 ${idx === 0 ? 'active' : ''}" data-img="${angle.img}">
          <div class="angle-thumb-wrapper">
            <img src="${angle.img}" alt="${angle.name} Angle">
          </div>
          <span class="angle-name">${angle.name}</span>
        </div>
      `).join('');
    } else if (data.main_img) {
      anglesGrid.innerHTML = `
        <div class="angle-card col-3 col-sm-6 active" data-img="${data.main_img}">
          <div class="angle-thumb-wrapper"><img src="${data.main_img}" alt="Front"></div>
          <span class="angle-name">Front</span>
        </div>`;
    }
    
    // Re-initialize the angle switcher with the new angle cards
    initAngleSwitcher();
  }

  if (galleryContainer && relatedStyles && relatedStyles.length) {
    galleryContainer.innerHTML = relatedStyles.map((style, idx) => `
      <a href="#" class="style-variation-card ${idx === 0 ? 'active' : ''}" data-slug="${style.slug}" data-title="${style.name}" data-img="${style.main_img}" style="text-decoration: none; color: inherit;">
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
