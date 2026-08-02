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
      genderModal.classList.add('active');
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

  // Capture canvas snapshot
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

  // Freeze live stream and display captured still photo preview
  if (videoElem) {
    videoElem.pause();
  }

  if (freezeImg && capturedImageDataUrl) {
    freezeImg.src = capturedImageDataUrl;
    freezeImg.style.display = 'block';
  }

  // Hide face frame guides during photo decision preview
  if (guideElem) guideElem.style.display = 'none';
  if (bracketsElem) bracketsElem.style.display = 'none';

  if (decisionContainer) decisionContainer.classList.add('active');
  if (controls) controls.style.display = 'none';

  // White camera shutter flash effect
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
}

function resetCameraState() {
  const decisionContainer = document.getElementById('captured-decision');
  const controls = document.getElementById('camera-controls-bar');
  const videoElem = document.getElementById('webcam-video');
  const freezeImg = document.getElementById('captured-freeze-img');
  const guideElem = document.querySelector('.face-overlay-guide');
  const bracketsElem = document.querySelector('.face-overlay-brackets');
  
  // Unfreeze video stream and hide still photo preview
  if (freezeImg) {
    freezeImg.style.display = 'none';
    freezeImg.src = '';
  }

  if (videoElem) {
    videoElem.play();
  }

  // Restore face frame guides
  if (guideElem) guideElem.style.display = 'block';
  if (bracketsElem) bracketsElem.style.display = 'block';

  if (decisionContainer) decisionContainer.classList.remove('active');
  if (controls) controls.style.display = 'flex';
}

async function submitCapturedPhoto(gender, analysisType) {
  const formData = new FormData();
  formData.append('image_base64', capturedImageDataUrl);
  formData.append('gender', gender);
  formData.append('analysis_type', analysisType);

  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    stopCamera();
    if (data.redirect_url) {
      window.location.href = data.redirect_url;
    } else {
      window.location.href = `/recommendation?gender=${gender}`;
    }
  } catch (err) {
    console.error("Camera submit error:", err);
    stopCamera();
    window.location.href = `/recommendation?gender=${gender}`;
  }
}
