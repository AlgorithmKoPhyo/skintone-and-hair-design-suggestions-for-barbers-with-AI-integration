/* ==========================================================================
   StyleMe - Barber & Stylist Reference Board Controller
   ========================================================================== */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', initBarberCard);

  function initBarberCard() {
    const modal    = document.getElementById('modal-barber-card');
    const openBtns = document.querySelectorAll('#btn-open-barber-card, .btn-open-barber-card');
    const closeBtn = document.getElementById('btn-close-barber-modal');
    const printBtn = document.getElementById('btn-print-barber-card');
    const imageBtn = document.getElementById('btn-save-image-barber-card');
    const shareBtn = document.getElementById('btn-share-barber-card');

    if (!modal) return;

    // Open Modal
    openBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        modal.classList.add('active');
      });
    });

    // Close Modal
    if (closeBtn) {
      closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    }

    // Close backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.classList.remove('active');
    });

    // Print / Save PDF
    if (printBtn) {
      printBtn.addEventListener('click', () => {
        window.print();
      });
    }

    // Save as PNG Image using html2canvas
    if (imageBtn) {
      imageBtn.addEventListener('click', () => {
        const printableArea = document.getElementById('barber-board-printable');
        if (!printableArea) return;

        if (imageBtn) {
          imageBtn.disabled = true;
          imageBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating PNG...';
        }

        if (typeof html2canvas === 'function') {
          html2canvas(printableArea, {
            scale: 2, // High resolution
            useCORS: true,
            backgroundColor: '#FAF8FF',
            onclone: function(clonedDoc) {
              const board = clonedDoc.getElementById('barber-board-printable');
              if (board) {
                // Force system fonts in the clone to fix html2canvas web font spacing bugs
                board.style.fontFamily = 'Arial, Helvetica, sans-serif';
                const elements = board.querySelectorAll('*');
                elements.forEach(el => {
                  el.style.fontFamily = 'Arial, Helvetica, sans-serif';
                  el.style.letterSpacing = 'normal';
                });
              }
            }
          }).then(canvas => {
            const link = document.createElement('a');
            link.download = 'StyleMe_Barber_Consultation_Card.png';
            link.href = canvas.toDataURL('image/png');
            link.click();

            if (imageBtn) {
              imageBtn.disabled = false;
              imageBtn.innerHTML = '<i class="fa-solid fa-file-image"></i> Save as Image (PNG)';
            }

            if (window.StyleMe && window.StyleMe.toast) {
              window.StyleMe.toast('Barber Board exported as PNG Image!', 'success');
            }
          }).catch(err => {
            console.error('Error generating image:', err);
            if (imageBtn) {
              imageBtn.disabled = false;
              imageBtn.innerHTML = '<i class="fa-solid fa-file-image"></i> Save as Image (PNG)';
            }
          });
        } else {
          alert('PNG Generator loading... Please try again in a moment.');
          if (imageBtn) {
            imageBtn.disabled = false;
            imageBtn.innerHTML = '<i class="fa-solid fa-file-image"></i> Save as Image (PNG)';
          }
        }
      });
    }

    // Share / Copy Text Specs to Clipboard
    if (shareBtn) {
      shareBtn.addEventListener('click', () => {
        const title    = document.getElementById('barber-card-title')?.textContent?.trim() || 'Hairstyle Reference';
        const tagline  = document.getElementById('barber-card-tagline')?.textContent?.trim() || '';
        const length   = document.getElementById('barber-card-length')?.textContent?.trim() || '';
        const texture  = document.getElementById('barber-card-texture')?.textContent?.trim() || '';
        const shape    = document.getElementById('barber-card-shape')?.textContent?.trim() || '';

        const textToCopy = `💈 StyleMe Barber Consultation Spec 💈\nHairstyle: ${title}\nTagline: ${tagline}\nHair Length: ${length}\nTexture: ${texture}\nIdeal Shape: ${shape}\nURL: ${window.location.href}`;

        if (navigator.clipboard) {
          navigator.clipboard.writeText(textToCopy).then(() => {
            if (window.StyleMe && window.StyleMe.toast) {
              window.StyleMe.toast('Barber spec details copied to clipboard!', 'success');
            } else {
              alert('Barber spec details copied to clipboard!');
            }
          });
        }
      });
    }
  }

  // Public API
  window.StyleMeBarber = {
    openModal: function() {
      const modal = document.getElementById('modal-barber-card');
      if (modal) modal.classList.add('active');
    }
  };
})();
