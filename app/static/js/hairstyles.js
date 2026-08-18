/* ==========================================================================
   StyleMe - All Hairstyles Catalog Filtering & Choose with AI Controller
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initCatalogFilters();
  initChooseWithAI();
});

function initCatalogFilters() {
  const genderBtns = document.querySelectorAll('[data-filter-gender]');
  const shapeSelect = document.getElementById('catalog-shape-select');
  const searchInput = document.getElementById('catalog-search-input');
  const categorySelect = document.getElementById('catalog-category-select');
  
  const grid = document.getElementById('hairstyles-catalog-grid');
  const loadingIndicator = document.getElementById('catalog-loading-indicator');
  const emptyState = document.getElementById('catalog-empty-state');
  const loadMoreContainer = document.getElementById('load-more-container');
  const loadMoreBtn = document.getElementById('load-more-btn');
  const countDisplay = document.getElementById('hairstyles-count-display');

  let activeGender = 'all';
  let activeShape = 'all';
  let activeCategory = 'all';
  let searchQuery = '';
  let currentPage = 1;
  const limit = 12;
  let isLoading = false;

  // Read URL query parameters for pre-filtering (e.g., ?shape=oval&gender=female)
  const urlParams = new URLSearchParams(window.location.search);
  const genderParam = urlParams.get('gender');
  const shapeParam = urlParams.get('shape');
  const categoryParam = urlParams.get('category');

  if (genderParam) {
    activeGender = genderParam;
    genderBtns.forEach(b => {
      if (b.getAttribute('data-filter-gender') === activeGender) b.classList.add('active');
      else b.classList.remove('active');
    });
  }

  if (shapeParam) {
    activeShape = shapeParam;
    if (shapeSelect) {
      shapeSelect.value = activeShape;
    }
  }

  if (categoryParam) {
    activeCategory = categoryParam;
    if (categorySelect) {
      categorySelect.value = activeCategory;
    }
  }

  const renderCard = (style) => {
    const genderIcon = style.gender === 'female' ? '<i class="fa-solid fa-venus"></i> Female' : '<i class="fa-solid fa-mars"></i> Male';
    const shapeBadge = style.shape_badge || `Ideal for ${style.faceshape ? style.faceshape.charAt(0).toUpperCase() + style.faceshape.slice(1) : ''} Face`;
    
    return `
      <div class="style-catalog-card col-4 col-md-6 col-sm-12" data-gender="${style.gender}" data-shape="${style.faceshape}" data-title="${style.name}">
        <div class="catalog-card-inner">
          <div class="catalog-img-wrapper" style="background: var(--bg-subtle, #f8fafc); display: flex; align-items: center; justify-content: center; aspect-ratio: 1 / 1; width: 100%; overflow: hidden; border-radius: var(--radius-md) var(--radius-md) 0 0; position: relative;">
            <img src="${style.main_img}" alt="${style.name}" style="width: 100%; height: 100%; object-fit: cover; object-position: center; transition: transform 0.5s ease;">
            <span style="position: absolute; top: 12px; left: 12px; background: rgba(15, 23, 42, 0.65); color: white; padding: 4px 12px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; backdrop-filter: blur(8px);">
              ${genderIcon}
            </span>
            <span style="position: absolute; top: 12px; right: 12px; background: linear-gradient(135deg, var(--purple-primary), #9333EA); color: white; padding: 4px 12px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);">
              ${shapeBadge}
            </span>
          </div>
          <div style="padding: 22px; display: flex; flex-direction: column; flex-grow: 1;">
            <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 6px; color: var(--text-main);">${style.name}</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 18px; flex-grow: 1; line-height: 1.5;">
              ${style.tagline || style.description || ''}
            </p>
            <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.82rem; color: var(--text-muted); border-top: 1px dashed var(--border-light); padding-top: 14px; margin-bottom: 18px;">
              <span><i class="fa-solid fa-ruler-vertical"></i> ${style.hair_length || 'Medium'}</span>
              <span style="background: rgba(245, 158, 11, 0.1); color: #D97706; padding: 3px 10px; border-radius: 9999px; font-weight: 700;">
                <i class="fa-solid fa-star"></i> ${style.score_badge || '95% Match'}
              </span>
            </div>
            <a href="/hairstyle-detail?style=${style.slug}&gender=${style.gender}" class="btn-details-pill">
              <i class="fa-solid fa-circle-info"></i> View Details
            </a>
          </div>
        </div>
      </div>
    `;
  };

  const fetchHairstyles = async (append = false) => {
    if (isLoading) return;
    isLoading = true;
    
    if (!append) {
      grid.innerHTML = '';
      currentPage = 1;
      emptyState.style.display = 'none';
    }
    
    loadMoreContainer.style.display = 'none';
    loadingIndicator.style.display = 'block';

    try {
      const url = new URL(window.location.origin + '/api/hairstyles');
      url.searchParams.append('gender', activeGender);
      url.searchParams.append('shape', activeShape);
      url.searchParams.append('category', activeCategory);
      url.searchParams.append('search', searchQuery);
      url.searchParams.append('page', currentPage);
      url.searchParams.append('limit', limit);

      const res = await fetch(url);
      const result = await res.json();
      
      loadingIndicator.style.display = 'none';
      
      if (result.status === 'success' && result.data.length > 0) {
        if (countDisplay && !append) {
          countDisplay.textContent = `${result.total} Hairstyles`;
        }
        const html = result.data.map(renderCard).join('');
        if (append) {
          grid.insertAdjacentHTML('beforeend', html);
        } else {
          grid.innerHTML = html;
        }
        
        if (currentPage < result.total_pages) {
          loadMoreContainer.style.display = 'block';
        }
      } else if (!append) {
        if (countDisplay) {
          countDisplay.textContent = `0 Hairstyles`;
        }
        emptyState.style.display = 'block';
      }
    } catch (err) {
      console.error("Error fetching hairstyles:", err);
      loadingIndicator.style.display = 'none';
    } finally {
      isLoading = false;
    }
  };

  // Initial fetch
  fetchHairstyles();

  loadMoreBtn.addEventListener('click', () => {
    currentPage++;
    fetchHairstyles(true);
  });

  let searchTimeout = null;
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = (e.target.value || '').trim().toLowerCase();
      if (searchTimeout) clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        fetchHairstyles(false);
      }, 300); // Debounce search
    });
  }

  if (categorySelect) {
    categorySelect.addEventListener('change', (e) => {
      activeCategory = e.target.value;
      fetchHairstyles(false);
    });
  }

  genderBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      genderBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeGender = btn.getAttribute('data-filter-gender');
      fetchHairstyles(false);
    });
  });

  if (shapeSelect) {
    shapeSelect.addEventListener('change', (e) => {
      activeShape = e.target.value;
      fetchHairstyles(false);
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
