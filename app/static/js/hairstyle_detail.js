/* ==========================================================================
   StyleMe - Hairstyle Detail Page Controller
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initDetailAngleSwitcher();
});

function initDetailAngleSwitcher() {
  const angleCards = document.querySelectorAll('.angle-card[data-detail-img]');
  const mainImg = document.getElementById('detail-main-img');

  angleCards.forEach(card => {
    card.addEventListener('click', () => {
      angleCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');

      const targetSrc = card.getAttribute('data-detail-img');
      if (mainImg && targetSrc) {
        mainImg.style.opacity = '0.3';
        setTimeout(() => {
          mainImg.src = targetSrc;
          mainImg.style.opacity = '1';
        }, 150);
      }
    });
  });
}
