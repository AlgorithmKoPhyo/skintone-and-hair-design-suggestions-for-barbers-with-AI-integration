/* ==========================================================================
   StyleMe - Hairstyle Detail Page Image Slider & Angle Switcher Controller
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initDetailImageSlider();
});

function initDetailImageSlider() {
  const mainImg       = document.getElementById('detail-main-img');
  const btnPrev       = document.getElementById('detail-slider-prev');
  const btnNext       = document.getElementById('detail-slider-next');
  const labelEl       = document.getElementById('detail-slider-label');
  const dotsContainer = document.getElementById('detail-slider-dots');
  const angleCards    = Array.from(document.querySelectorAll('.angle-card[data-detail-img]'));

  if (!mainImg || angleCards.length === 0) return;

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
    const targetSrc  = activeCard.getAttribute('data-detail-img');
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
    if (mainImg && targetSrc && mainImg.src !== targetSrc) {
      mainImg.style.opacity = '0.2';
      setTimeout(() => {
        mainImg.src = targetSrc;
        mainImg.style.opacity = '1';
      }, 140);
    }
  }

  // Next / Prev button click listeners
  if (btnPrev) {
    btnPrev.addEventListener('click', (e) => {
      e.stopPropagation();
      goToIndex(currentIndex - 1);
    });
  }

  if (btnNext) {
    btnNext.addEventListener('click', (e) => {
      e.stopPropagation();
      goToIndex(currentIndex + 1);
    });
  }

  // Click on thumbnail card
  angleCards.forEach((card, idx) => {
    card.addEventListener('click', () => goToIndex(idx));
  });

  // Touch Swipe Gesture & Auto-play Support
  const wrapper = mainImg.closest('.rec-preview-wrapper');
  let autoTimer = null;

  function startAutoPlay() {
    stopAutoPlay();
    autoTimer = setInterval(() => {
      goToIndex(currentIndex + 1);
    }, 4000);
  }

  function stopAutoPlay() {
    if (autoTimer) {
      clearInterval(autoTimer);
      autoTimer = null;
    }
  }

  startAutoPlay();

  if (wrapper) {
    wrapper.addEventListener('mouseenter', stopAutoPlay);
    wrapper.addEventListener('mouseleave', startAutoPlay);

    let touchStartX = 0;
    let touchEndX = 0;

    wrapper.addEventListener('touchstart', (e) => {
      stopAutoPlay();
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    wrapper.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
      startAutoPlay();
    }, { passive: true });

    function handleSwipe() {
      const diff = touchEndX - touchStartX;
      if (Math.abs(diff) > 40) {
        if (diff < 0) goToIndex(currentIndex + 1); // Swipe left → Next
        else goToIndex(currentIndex - 1);          // Swipe right → Prev
      }
    }
  }

  // Keyboard Left / Right arrow navigation
  document.addEventListener('keydown', (e) => {
    if (document.activeElement && ['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
    if (e.key === 'ArrowLeft') goToIndex(currentIndex - 1);
    if (e.key === 'ArrowRight') goToIndex(currentIndex + 1);
  });
}

