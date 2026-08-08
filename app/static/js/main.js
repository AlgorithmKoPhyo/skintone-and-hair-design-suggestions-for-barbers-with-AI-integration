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

console.log('StyleMe loaded.');
