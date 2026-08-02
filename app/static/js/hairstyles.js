/* ==========================================================================
   StyleMe - All Hairstyles Catalog Filtering & Choose with AI Controller
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initCatalogFilters();
  initChooseWithAI();
});

function initCatalogFilters() {
  const genderBtns = document.querySelectorAll('[data-filter-gender]');
  const shapeBtns = document.querySelectorAll('[data-filter-shape]');
  const searchInput = document.getElementById('catalog-search-input');
  const styleCards = document.querySelectorAll('.style-catalog-card');

  let activeGender = 'all';
  let activeShape = 'all';
  let searchQuery = '';

  const filterCards = () => {
    styleCards.forEach(card => {
      const cardGender = card.getAttribute('data-gender');
      const cardShape = card.getAttribute('data-shape');
      const cardTitle = (card.getAttribute('data-title') || '').toLowerCase();

      const matchesGender = (activeGender === 'all' || cardGender === activeGender);
      const matchesShape = (activeShape === 'all' || cardShape === activeShape);
      const matchesSearch = (searchQuery === '' || cardTitle.includes(searchQuery));

      if (matchesGender && matchesShape && matchesSearch) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  };

  // Read URL query parameters for pre-filtering (e.g., ?shape=oval&gender=female)
  const urlParams = new URLSearchParams(window.location.search);
  const genderParam = urlParams.get('gender');
  const shapeParam = urlParams.get('shape');

  if (genderParam) {
    activeGender = genderParam;
    genderBtns.forEach(b => {
      if (b.getAttribute('data-filter-gender') === activeGender) {
        b.classList.add('active');
      } else {
        b.classList.remove('active');
      }
    });
  }

  if (shapeParam) {
    activeShape = shapeParam;
    shapeBtns.forEach(b => {
      if (b.getAttribute('data-filter-shape') === activeShape) {
        b.classList.add('active');
      } else {
        b.classList.remove('active');
      }
    });
  }

  // Run initial pre-filtered display
  filterCards();

  genderBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      genderBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeGender = btn.getAttribute('data-filter-gender');
      filterCards();
    });
  });

  shapeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      shapeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeShape = btn.getAttribute('data-filter-shape');
      filterCards();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = (e.target.value || '').trim().toLowerCase();
      filterCards();
    });
  }
}

function initChooseWithAI() {
  const triggers = document.querySelectorAll('.btn-choose-ai-trigger');
  const modal = document.getElementById('modal-choose-ai');
  const modalTitle = document.getElementById('choose-ai-modal-title');
  const fileInput = document.getElementById('choose-ai-file-input');
  const btnUpload = document.getElementById('btn-choose-ai-upload');

  let currentTargetGender = 'female';
  let currentTargetShape = 'oval';

  triggers.forEach(btn => {
    btn.addEventListener('click', () => {
      const styleName = btn.getAttribute('data-style-name') || 'Style';
      currentTargetGender = btn.getAttribute('data-gender') || 'female';
      currentTargetShape = btn.getAttribute('data-shape') || 'oval';

      if (modalTitle) {
        modalTitle.textContent = `Try ${styleName} With AI`;
      }
      if (modal) {
        modal.classList.add('active');
      }
    });
  });

  if (btnUpload && fileInput) {
    btnUpload.addEventListener('click', () => {
      fileInput.click();
    });

    fileInput.addEventListener('change', async (e) => {
      if (e.target.files && e.target.files[0]) {
        const file = e.target.files[0];
        btnUpload.disabled = true;
        btnUpload.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

        const formData = new FormData();
        formData.append('image', file);
        formData.append('gender', currentTargetGender);
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
            window.location.href = `/recommendation?gender=${currentTargetGender}&shape=${currentTargetShape}`;
          }
        } catch (err) {
          console.error("Choose with AI upload error:", err);
          window.location.href = `/recommendation?gender=${currentTargetGender}&shape=${currentTargetShape}`;
        }
      }
    });
  }

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
      }
    });
  }
}
