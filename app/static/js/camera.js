/* ==========================================================================
   StyleMe - Live Camera & Photo Capture Controller (Frozen Still Preview)
   ========================================================================== */

let currentStream = null;
let currentFacingMode = 'user';
let capturedImageDataUrl = '';

document.addEventListener('DOMContentLoaded', () => {
  initLiveCamera();
});

function initLiveCamera() {
  const videoElem = document.getElementById('webcam-video');
  const btnShutter = document.getElementById('btn-shutter');
  const btnFlipCam = document.getElementById('btn-flip-cam');
  const btnRetake = document.getElementById('btn-retake');
  const btnChooseHairstyle = document.getElementById('btn-choose-hairstyle-trigger');
  const btnChooseColor = document.getElementById('btn-choose-color-trigger');
  const genderModal = document.getElementById('modal-gender-select');
  const btnOptFemale = document.getElementById('gender-opt-female');
  const btnOptMale = document.getElementById('gender-opt-male');

  if (videoElem) {
    startCamera();
  }

  if (btnShutter) {
    btnShutter.addEventListener('click', capturePhoto);
  }

  if (btnFlipCam) {
    btnFlipCam.addEventListener('click', toggleCameraFlip);
  }

  if (btnRetake) {
    btnRetake.addEventListener('click', resetCameraState);
  }

  // Open Gender Selection Modal when clicking "Choose Hairstyle"
  if (btnChooseHairstyle && genderModal) {
    btnChooseHairstyle.addEventListener('click', () => {
      const optColor = document.getElementById('opt-color-analysis');
      if (optColor) optColor.style.display = 'none';
      const modalTitle = document.getElementById('gender-modal-title');
      if (modalTitle) modalTitle.textContent = "Select Gender Preference";
      const modalSubtitle = document.getElementById('gender-modal-subtitle');
      if (modalSubtitle) modalSubtitle.textContent = "Which hairstyle collection would you like our AI to recommend for your face shape?";
      genderModal.classList.add('active');
    });
  }

  // Handle "Choose Color Analysis" directly from camera flow
  if (btnChooseColor) {
    btnChooseColor.addEventListener('click', async () => {
      await submitCapturedPhoto('female', 'color');
    });
  }

  // Handle Gender selection inside modal
  if (btnOptFemale) {
    btnOptFemale.addEventListener('click', async () => {
      if (genderModal) genderModal.classList.remove('active');
      await submitCapturedPhoto('female', 'hairstyle');
    });
  }

  if (btnOptMale) {
    btnOptMale.addEventListener('click', async () => {
      if (genderModal) genderModal.classList.remove('active');
      await submitCapturedPhoto('male', 'hairstyle');
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

  // Inject the camera-side validation banner into the decision panel (once)
  _injectCameraValidationBanner();
}

// ---- Inject validation banner into camera decision panel -----------------
function _injectCameraValidationBanner() {
  const decisionPanel = document.getElementById('captured-decision');
  if (!decisionPanel || document.getElementById('cam-face-validation-banner')) return;

  // Scanning indicator
  const scanRow = document.createElement('div');
  scanRow.id = 'cam-face-scan-status';
  scanRow.style.cssText = 'display:none; align-items:center; gap:10px; background:var(--purple-light); border:1px solid rgba(124,58,237,0.18); border-radius:10px; padding:9px 14px; margin-bottom:14px; font-size:0.82rem; font-weight:600; color:var(--purple-primary);';
  scanRow.innerHTML = '<div style="width:14px;height:14px;border:2px solid rgba(124,58,237,0.25);border-top-color:var(--purple-primary);border-radius:50%;animation:spin 0.8s linear infinite;flex-shrink:0;"></div><span>Checking for a face in your photo…</span>';

  // Warning banner
  const warnRow = document.createElement('div');
  warnRow.id = 'cam-face-validation-banner';
  warnRow.style.cssText = 'display:none; align-items:flex-start; gap:10px; background:#FFF7ED; border:1.5px solid #FB923C; border-radius:12px; padding:11px 14px; margin-bottom:14px; text-align:left;';
  warnRow.innerHTML = '<i class="fa-solid fa-triangle-exclamation" style="color:#EA580C;font-size:1rem;flex-shrink:0;margin-top:2px;"></i><div><div style="font-weight:700;font-size:0.83rem;color:#9A3412;margin-bottom:2px;">No face detected</div><div id="cam-face-validation-msg" style="font-size:0.78rem;color:#C2410C;line-height:1.4;">Please retake the photo with your face clearly visible.</div></div>';

  decisionPanel.insertBefore(warnRow, decisionPanel.firstChild);
  decisionPanel.insertBefore(scanRow, decisionPanel.firstChild);
}

// ---- Camera validation UI state ------------------------------------------
function setCameraValidationState(state, message) {
  const scanStatus = document.getElementById('cam-face-scan-status');
  const warnBanner = document.getElementById('cam-face-validation-banner');
  const msgEl = document.getElementById('cam-face-validation-msg');
  const btnHairstyle = document.getElementById('btn-choose-hairstyle-trigger');
  const btnColor = document.getElementById('btn-choose-color-trigger');
  const capturedTitle = document.querySelector('.captured-title p');

  if (scanStatus) scanStatus.style.display = 'none';
  if (warnBanner) warnBanner.style.display = 'none';

  if (state === 'scanning') {
    if (scanStatus) scanStatus.style.display = 'flex';
    if (btnHairstyle) btnHairstyle.disabled = true;
    if (btnColor) btnColor.disabled = true;
    if (capturedTitle) capturedTitle.textContent = 'Checking your photo for a face…';

  } else if (state === 'valid') {
    if (btnHairstyle) btnHairstyle.disabled = false;
    if (btnColor) btnColor.disabled = false;
    if (capturedTitle) capturedTitle.textContent = 'What would you like to get recommendation for?';

  } else if (state === 'invalid') {
    if (warnBanner) warnBanner.style.display = 'flex';
    if (msgEl && message) msgEl.textContent = message;
    if (btnHairstyle) btnHairstyle.disabled = true;
    if (btnColor) btnColor.disabled = true;
    if (capturedTitle) capturedTitle.textContent = 'Please retake the photo with your face clearly visible.';
  }
}

// ---- Background face validation for captured image -----------------------
async function validateCapturedFace() {
  setCameraValidationState('scanning');
  try {
    const blob = await fetch(capturedImageDataUrl).then(r => r.blob());
    const formData = new FormData();
    formData.append('image', blob, 'captured.jpg');

    const res = await fetch('/validate-face', { method: 'POST', body: formData });
    const data = await res.json();

    if (data.valid) {
      setCameraValidationState('valid');
    } else {
      setCameraValidationState('invalid', data.message || 'No face detected. Please retake the photo with your face clearly visible.');
    }
  } catch (err) {
    console.warn('[StyleMe] /validate-face (camera) failed, failing open:', err);
    setCameraValidationState('valid');
  }
}

async function startCamera() {
  const videoElem = document.getElementById('webcam-video');
  const sampleImg = document.getElementById('camera-sample-img');
  resetCameraState();

  try {
    const constraints = {
      video: { facingMode: currentFacingMode, width: { ideal: 1280 }, height: { ideal: 720 } }
    };
    currentStream = await navigator.mediaDevices.getUserMedia(constraints);
    if (videoElem) {
      videoElem.srcObject = currentStream;
      videoElem.style.display = 'block';
      if (sampleImg) sampleImg.style.display = 'none';
    }
  } catch (err) {
    console.warn("Camera access unavailable or denied. Using high quality sample photo mode:", err);
    if (videoElem) videoElem.style.display = 'none';
    if (sampleImg) sampleImg.style.display = 'block';
  }
}

function stopCamera() {
  if (currentStream) {
    currentStream.getTracks().forEach(track => track.stop());
    currentStream = null;
  }
}

function toggleCameraFlip() {
  currentFacingMode = (currentFacingMode === 'user') ? 'environment' : 'user';
  if (currentStream) {
    stopCamera();
    startCamera();
  }
}

function capturePhoto() {
  const shutterBtn = document.getElementById('btn-shutter');
  const decisionContainer = document.getElementById('captured-decision');
  const controls = document.getElementById('camera-controls-bar');
  const videoElem = document.getElementById('webcam-video');
  const sampleImg = document.getElementById('camera-sample-img');
  const freezeImg = document.getElementById('captured-freeze-img');
  const guideElem = document.querySelector('.face-overlay-guide');
  const bracketsElem = document.querySelector('.face-overlay-brackets');

  if (shutterBtn) shutterBtn.style.transform = 'scale(0.85)';
  setTimeout(() => { if (shutterBtn) shutterBtn.style.transform = 'scale(1)'; }, 150);

  try {
    const canvas = document.createElement('canvas');
    if (videoElem && videoElem.style.display !== 'none' && videoElem.videoWidth) {
      canvas.width = videoElem.videoWidth;
      canvas.height = videoElem.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(videoElem, 0, 0, canvas.width, canvas.height);
      capturedImageDataUrl = canvas.toDataURL('image/jpeg', 0.9);
    } else if (sampleImg) {
      capturedImageDataUrl = sampleImg.src;
    }
  } catch (e) {
    console.warn("Canvas capture exception:", e);
  }

  if (videoElem) {
    videoElem.pause();
  }

  if (freezeImg && capturedImageDataUrl) {
    freezeImg.src = capturedImageDataUrl;
    freezeImg.style.display = 'block';
  }

  if (guideElem) guideElem.style.display = 'none';
  if (bracketsElem) bracketsElem.style.display = 'none';

  if (decisionContainer) decisionContainer.classList.add('active');
  if (controls) controls.style.display = 'none';

  const viewport = document.querySelector('.camera-viewport');
  if (viewport) {
    const flash = document.createElement('div');
    flash.style.position = 'absolute';
    flash.style.top = '0'; flash.style.left = '0'; flash.style.right = '0'; flash.style.bottom = '0';
    flash.style.background = '#fff'; flash.style.zIndex = '15'; flash.style.opacity = '0.85';
    flash.style.transition = 'opacity 0.35s ease';
    viewport.appendChild(flash);
    setTimeout(() => { flash.style.opacity = '0'; setTimeout(() => flash.remove(), 350); }, 50);
  }

  validateCapturedFace();
}

function resetCameraState() {
  const decisionContainer = document.getElementById('captured-decision');
  const controls = document.getElementById('camera-controls-bar');
  const videoElem = document.getElementById('webcam-video');
  const freezeImg = document.getElementById('captured-freeze-img');
  const guideElem = document.querySelector('.face-overlay-guide');
  const bracketsElem = document.querySelector('.face-overlay-brackets');

  if (freezeImg) {
    freezeImg.style.display = 'none';
    freezeImg.src = '';
  }

  if (videoElem) {
    videoElem.play();
  }

  if (guideElem) guideElem.style.display = 'block';
  if (bracketsElem) bracketsElem.style.display = 'block';

  if (decisionContainer) decisionContainer.classList.remove('active');
  if (controls) controls.style.display = 'flex';

  const scanStatus = document.getElementById('cam-face-scan-status');
  const warnBanner = document.getElementById('cam-face-validation-banner');
  if (scanStatus) scanStatus.style.display = 'none';
  if (warnBanner) warnBanner.style.display = 'none';
  const capturedTitle = document.querySelector('.captured-title p');
  if (capturedTitle) capturedTitle.textContent = 'What would you like to get recommendation for?';
}

// ── Fixed Submit Function ──────────────────────────────────────────────────
async function submitCapturedPhoto(gender, analysisType) {
  const formData = new FormData();

  try {
    const resBlob = await fetch(capturedImageDataUrl).then(res => res.blob());
    formData.append('image', resBlob, 'photo.jpg');
    formData.append('gender', gender);
    formData.append('analysis_type', analysisType);

    // Save the captured live camera photo to session storage
    if (capturedImageDataUrl) {
      sessionStorage.setItem('styleme_captured_image', capturedImageDataUrl);
    }

    const res = await fetch('/analyze', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) throw new Error('Network response was not ok');

    const data = await res.json();
    stopCamera();

    if (data.redirect_url) {
      window.location.href = data.redirect_url;
    } else {
      if (analysisType === 'color') {
        window.location.href = data.color_url || '/color-analysis';
      } else {
        window.location.href = `/recommendation?gender=${gender}`;
      }
    }
  } catch (err) {
    console.error("Camera submit error:", err);
    stopCamera();
    if (capturedImageDataUrl) {
      sessionStorage.setItem('styleme_captured_image', capturedImageDataUrl);
    }
    if (analysisType === 'color') {
      window.location.href = '/color-analysis';
    } else {
      window.location.href = `/recommendation?gender=${gender}`;
    }
  }
}