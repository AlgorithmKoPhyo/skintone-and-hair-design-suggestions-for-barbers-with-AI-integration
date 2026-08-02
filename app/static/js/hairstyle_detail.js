/* ==========================================================================
   StyleMe - Hairstyle Detail Page Controller
   ========================================================================== */

const hairstyleDetailCatalog = {
  classic_bob: {
    name: "Classic Bob Cut",
    tagline: "Timeless chin-length cut enhancing natural symmetry.",
    gender: "female",
    shapeBadge: "Oval & Heart Choice",
    scoreBadge: "95% Match Score",
    mainImg: "/static/images/classic_bob.jpg",
    desc: "A classic bob cut features clean perimeter lines falling between the chin and collarbone. It creates a framing silhouette that enhances cheekbones and balances facial proportions with effortless sophistication.",
    suitability: [
      { shape: "Oval Face", score: "95% (Ideal)" },
      { shape: "Heart Face", score: "92% (Great)" },
      { shape: "Round Face", score: "85% (Good)" },
      { shape: "Square Face", score: "80% (Moderate)" }
    ],
    specs: {
      length: "Chin to Shoulder",
      texture: "Straight / Soft Waves",
      time: "10 - 15 mins",
      maint: "Easy (Trim 6-8 Weeks)"
    },
    tips: [
      "Blow dry with a round brush for inward natural end curves.",
      "Tuck one side behind the ear for an effortless chic look.",
      "Use heat protectant spray before using flat irons or curling wands.",
      "A lightweight finishing oil keeps ends glossy and smooth."
    ]
  },
  textured_bob: {
    name: "Textured Long Bob (Lob)",
    tagline: "Collarbone length with subtle layers elongating face shape.",
    gender: "female",
    shapeBadge: "Round Face Choice",
    scoreBadge: "92% Match Score",
    mainImg: "/static/images/textured_bob.jpg",
    desc: "A textured long bob (lob) creates vertical length while gentle texturizing softens side cheek curves. Perfect for adding height at the crown.",
    suitability: [
      { shape: "Round Face", score: "92% (Ideal)" },
      { shape: "Oval Face", score: "90% (Great)" },
      { shape: "Heart Face", score: "88% (Great)" },
      { shape: "Square Face", score: "84% (Good)" }
    ],
    specs: {
      length: "Collarbone Length",
      texture: "Textured / Wavy",
      time: "15 mins",
      maint: "Moderate"
    },
    tips: [
      "Use texturizing sea salt spray for beachy wave definition.",
      "Opt for an off-center or side part to break symmetry.",
      "Curtain bangs draw emphasis to eyes and cheekbones."
    ]
  },
  layered_bob: {
    name: "Layered Soft Bob",
    tagline: "Feathered soft layers softening strong square angles.",
    gender: "female",
    shapeBadge: "Square Face Choice",
    scoreBadge: "94% Match Score",
    mainImg: "/static/images/layered_bob.jpg",
    desc: "Feathered layers around the jawline break up sharp angular jaw lines while adding romantic movement and gentle dimension.",
    suitability: [
      { shape: "Square Face", score: "94% (Ideal)" },
      { shape: "Oval Face", score: "91% (Great)" },
      { shape: "Heart Face", score: "87% (Good)" },
      { shape: "Round Face", score: "82% (Good)" }
    ],
    specs: {
      length: "Past Jawline",
      texture: "Soft Layers / Waves",
      time: "10 - 15 mins",
      maint: "Easy"
    },
    tips: [
      "Style with inward curving ends to hug the jawline.",
      "Side-swept bangs complement feathered layers.",
      "Incorporate subtle highlights for soft multi-dimensional texture."
    ]
  },
  french_bob: {
    name: "French A-Line Bob",
    tagline: "Chic French cut with soft chin volume.",
    gender: "female",
    shapeBadge: "Heart Face Choice",
    scoreBadge: "96% Match Score",
    mainImg: "/static/images/french_bob.jpg",
    desc: "Classic Parisian silhouette featuring wispy bangs and jaw-length fullness that complements heart-shaped cheekbones and narrow chins.",
    suitability: [
      { shape: "Heart Face", score: "96% (Ideal)" },
      { shape: "Oval Face", score: "93% (Great)" },
      { shape: "Round Face", score: "85% (Good)" },
      { shape: "Square Face", score: "81% (Moderate)" }
    ],
    specs: {
      length: "Jaw to Chin Length",
      texture: "Straight or Soft Curl",
      time: "10 mins",
      maint: "Easy"
    },
    tips: [
      "Inward curled ends bring weight right where your chin needs it.",
      "Wispy full bangs disguise a wider hairline.",
      "Keep crown volume subtle so top doesn't look top-heavy."
    ]
  },
  male_crop: {
    name: "Textured Crop Fade",
    tagline: "Clean side taper paired with textured top volume.",
    gender: "male",
    shapeBadge: "Oval Face Choice",
    scoreBadge: "97% Match Score",
    mainImg: "/static/images/male_crop.jpg",
    desc: "A modern textured crop with tapered sides highlights natural male facial symmetry while keeping maintenance minimal.",
    suitability: [
      { shape: "Oval Face", score: "97% (Ideal)" },
      { shape: "Round Face", score: "94% (Great)" },
      { shape: "Square Face", score: "90% (Great)" },
      { shape: "Heart Face", score: "88% (Good)" }
    ],
    specs: {
      length: "Short Top, Tapered Sides",
      texture: "Textured Crop",
      time: "5 mins",
      maint: "Low (Trim 2-3 Weeks)"
    },
    tips: [
      "Apply matte clay or styling paste for natural texture.",
      "Blow dry upward at the roots for lightweight volume.",
      "Keep side tapers clean for sharp contrast."
    ]
  },
  male_side_part: {
    name: "Classic Side Part",
    tagline: "Sleek masculine side part with subtle taper.",
    gender: "male",
    shapeBadge: "Square Face Choice",
    scoreBadge: "96% Match Score",
    mainImg: "/static/images/male_side_part.jpg",
    desc: "A timeless executive side part with neat tapered sides that accentuates strong jawlines with refined professional elegance.",
    suitability: [
      { shape: "Square Face", score: "96% (Ideal)" },
      { shape: "Oval Face", score: "94% (Great)" },
      { shape: "Round Face", score: "89% (Good)" },
      { shape: "Heart Face", score: "86% (Good)" }
    ],
    specs: {
      length: "Short to Medium",
      texture: "Sleek Side Part",
      time: "5 - 10 mins",
      maint: "Easy"
    },
    tips: [
      "Comb hair along natural side part while damp.",
      "Use medium-shine pomade for a polished finish.",
      "Keep neckline neatly trimmed."
    ]
  }
};

document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const styleId = urlParams.get('style') || 'classic_bob';

  if (hairstyleDetailCatalog[styleId]) {
    populateDetailView(hairstyleDetailCatalog[styleId]);
  }

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

function populateDetailView(data) {
  const titleElem = document.getElementById('detail-style-name');
  const taglineElem = document.getElementById('detail-tagline');
  const badgeShape = document.getElementById('detail-badge-shape');
  const badgeSub = document.getElementById('detail-badge-sub');
  const mainImg = document.getElementById('detail-main-img');
  const headingTitle = document.getElementById('detail-heading-title');
  const headingTagline = document.getElementById('detail-heading-tagline');
  const descText = document.getElementById('detail-desc-text');
  const suitabilityChecklist = document.getElementById('detail-suitability-checklist');
  const specLength = document.getElementById('detail-spec-length');
  const specTexture = document.getElementById('detail-spec-texture');
  const specTime = document.getElementById('detail-spec-time');
  const specMaint = document.getElementById('detail-spec-maint');
  const tipsList = document.getElementById('detail-tips-list');
  const tryBtn = document.getElementById('detail-btn-try');

  if (titleElem) titleElem.innerHTML = `${data.name} <i class="fa-solid fa-scissors" style="color: var(--purple-primary); font-size: 1.8rem; margin-left: 6px;"></i>`;
  if (taglineElem) taglineElem.textContent = data.tagline;
  if (badgeShape) badgeShape.textContent = data.shapeBadge;
  if (badgeSub) badgeSub.textContent = data.scoreBadge;
  if (mainImg) mainImg.src = data.mainImg;
  if (headingTitle) headingTitle.textContent = data.name;
  if (headingTagline) headingTagline.textContent = data.tagline;
  if (descText) descText.textContent = data.desc;

  if (suitabilityChecklist && data.suitability) {
    suitabilityChecklist.innerHTML = data.suitability.map(s => `
      <li>
        <span class="check-icon"><i class="fa-solid fa-check"></i></span>
        <span>${s.shape}: <strong style="color: var(--purple-primary);">${s.score}</strong></span>
      </li>
    `).join('');
  }

  if (specLength) specLength.textContent = data.specs.length;
  if (specTexture) specTexture.textContent = data.specs.texture;
  if (specTime) specTime.textContent = data.specs.time;
  if (specMaint) specMaint.textContent = data.specs.maint;

  if (tipsList && data.tips) {
    tipsList.innerHTML = data.tips.map(t => `<li>${t}</li>`).join('');
  }

  if (tryBtn) {
    tryBtn.href = `/recommendation?gender=${data.gender}`;
  }
}
