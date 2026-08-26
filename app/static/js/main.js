/* ==========================================================================
   StyleMe - Global Application Utilities
   - ESC key closes any open modal
   - Toast notification system
   ========================================================================== */

// ── ESC key closes any active modal ────────────────────────────────────────
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-backdrop.active').forEach(modal => {
      modal.classList.remove('active');
    });
    // Also reset gender_upload pending state if available
    if (window.StyleMeGender) {
      window.StyleMeGender.closeModal();
    }
  }
});

// ── Toast Notification System ───────────────────────────────────────────────
// Usage: StyleMe.toast('Message', 'success' | 'error' | 'info')
window.StyleMe = window.StyleMe || {};

StyleMe.toast = function (message, type = 'info', duration = 3500) {
  // Create container if it doesn't exist
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    `;
    document.body.appendChild(container);
  }

  const colors = {
    success: { bg: '#ECFDF5', border: '#10B981', text: '#065F46', icon: 'fa-circle-check' },
    error:   { bg: '#FEF2F2', border: '#EF4444', text: '#991B1B', icon: 'fa-circle-xmark' },
    info:    { bg: '#EDE9FE', border: '#7C3AED', text: '#4C1D95', icon: 'fa-circle-info'  },
  };
  const c = colors[type] || colors.info;

  const toast = document.createElement('div');
  toast.style.cssText = `
    background: ${c.bg};
    border: 1.5px solid ${c.border};
    color: ${c.text};
    padding: 12px 18px;
    border-radius: 14px;
    font-size: 0.875rem;
    font-weight: 600;
    font-family: var(--font-primary, sans-serif);
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    pointer-events: all;
    opacity: 0;
    transform: translateY(12px);
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    min-width: 240px;
    max-width: 360px;
  `;
  toast.innerHTML = `<i class="fa-solid ${c.icon}" style="font-size:1rem;flex-shrink:0;"></i><span>${message}</span>`;
  container.appendChild(toast);

  // Animate in
  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';
  });

  // Dismiss
  const dismiss = () => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(8px)';
    setTimeout(() => toast.remove(), 300);
  };

  setTimeout(dismiss, duration);
  toast.addEventListener('click', dismiss);
};

// ── Cross Analysis Utility ───────────────────────────────────────────────────
window.runCrossAnalysis = async function (analysisType, imageUrl, gender) {
  if (!imageUrl || imageUrl === '#' || imageUrl.includes('default_user')) {
    StyleMe.toast("Please capture or upload a photo first.", "error");
    return;
  }

  // Show loading indicator via modal
  const modalId = 'cross-analysis-loading-modal';
  let modal = document.getElementById(modalId);
  if (!modal) {
    modal = document.createElement('div');
    modal.id = modalId;
    modal.className = 'modal-backdrop active';
    document.body.appendChild(modal);
  } else {
    modal.classList.add('active');
  }

  // Reset modal content to spinner
  modal.innerHTML = `
    <div class="modal-card" style="padding: 40px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px; text-align: center; max-width: 400px; border-radius: 20px;">
      <div style="width: 60px; height: 60px; border: 4px solid var(--purple-light); border-top-color: var(--purple-primary); border-radius: 50%; animation: spin 0.9s linear infinite;"></div>
      <h3 style="margin: 0; color: var(--text-main); font-size: 1.3rem; font-weight: 700;">Analyzing your photo...</h3>
      <p style="margin: 0; color: var(--text-muted); font-size: 0.95rem; line-height: 1.5;">Please wait while our AI processes your image.</p>
    </div>
  `;

  const showError = (msg) => {
    modal.innerHTML = `
      <div class="modal-card" style="padding: 40px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; text-align: center; max-width: 420px; border-radius: 20px;">
        <div style="width: 64px; height: 64px; border-radius: 50%; background: #FEE2E2; color: #EF4444; display: flex; align-items: center; justify-content: center; font-size: 2rem; margin-bottom: 4px;">
          <i class="fa-solid fa-triangle-exclamation"></i>
        </div>
        <h3 style="margin: 0; color: var(--text-main); font-size: 1.35rem; font-weight: 700;">Analysis Error</h3>
        <p style="margin: 0; color: var(--text-muted); font-size: 0.95rem; line-height: 1.5;">${msg}</p>
        <div style="display: flex; gap: 12px; margin-top: 16px; width: 100%;">
          <button onclick="document.getElementById('${modalId}').classList.remove('active');" style="flex: 1; padding: 12px; border-radius: 12px; border: 1.5px solid var(--border-light); background: transparent; color: var(--text-muted); cursor: pointer; font-weight: 600; font-family: inherit; font-size: 0.95rem;">Cancel</button>
          <a href="/camera" style="flex: 1; padding: 12px; border-radius: 12px; border: none; background: var(--purple-primary); color: white; cursor: pointer; font-weight: 600; font-family: inherit; font-size: 0.95rem; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 8px;"><i class="fa-solid fa-camera"></i> Retake Photo</a>
        </div>
      </div>
    `;
  };

  try {
    const formData = new FormData();
    formData.append('existing_image_url', imageUrl);
    formData.append('gender', gender);
    formData.append('analysis_type', analysisType);

    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    
    if (!response.ok || data.status === 'error') {
      showError(data.message || "Failed to perform analysis. Please try again.");
      return;
    }

    if (data.redirect_url) {
      window.location.href = data.redirect_url;
    } else {
      showError("Analysis complete, but no redirect provided.");
    }
  } catch (error) {
    console.error("Cross analysis error:", error);
    showError("Failed to perform analysis. Please try again.");
  }
};

console.log('StyleMe loaded.');
