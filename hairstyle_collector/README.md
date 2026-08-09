# StyleMe AI - Centralized Hairstyle Data Collector

An isolated, standalone Vue 3 Single File Component (SFC) single-page web application built with Vite, Cloudinary CDN, and Firebase Firestore. This application provides a high-performance administrative interface for managing multi-angle hairstyle assets, face shape suitability matrices, styling recommendations, and catalog metadata.

---

## Technical Stack

- Core Framework: Vue 3 (Composition API with `<script setup>`)
- Build Tool & Dev Server: Vite
- Routing: Vue Router with HTML5 Web History (`createWebHistory`)
- Storage & CDN: Cloudinary Unsigned Direct API (Multi-angle photos)
- Database: Firebase Firestore v10 Modular SDK
- Styling: Vanilla CSS with custom design system variables matching the main application palette

---

## Key Features

1. Modern Data Catalog Table:
   - Paginated table view supporting 5, 10, 25, or 50 records per page.
   - Comprehensive metadata display including main thumbnail, title, URL slug, variation name, badges, specifications, 4-angle photo grid, description, and action buttons.
   - Expandable sub-row drawer displaying recommendation checklists, styling tips, and face shape suitability score matrices.
   - Filter toolbar supporting real-time text search, face shape filtering, gender filtering, and usage status filtering.

2. Usage Status and Edit Protection:
   - Supports Usage Status designation: `main_page` (Published / Live) vs `draft` (Editable Draft).
   - Main Page Edit Locking Rule: Records marked for `main_page` usage are locked from editing in the Data Collector to prevent accidental modification of production data.

3. Direct Cloudinary CDN Photo Uploads:
   - Direct browser-to-Cloudinary CDN image streaming without passing image binary through intermediate Node servers.
   - Zero Base64 in Database Rule: Firebase Firestore stores only lightweight CDN URL strings (under 100 bytes each) to adhere to Firestore document size limits.

4. Interactive Progress Overlay:
   - Dedicated Saving Modal popup showing step-by-step progress bars (0% to 100%) during photo upload and metadata synchronization.

5. Image Lightbox Modal:
   - High-resolution click-to-enlarge lightbox popup for inspecting 4-angle photos and main cover thumbnails.

6. Data Export:
   - One-click JSON exporter for downloading all catalog records into a structured JSON file.

---

## Quick Start (Local Development)

### 1. Environment Configuration

Create a `.env` file in the `hairstyle_collector` root directory based on `.env.example`:

```env
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id

VITE_CLOUDINARY_CLOUD_NAME=your_cloud_name
VITE_CLOUDINARY_UPLOAD_PRESET=styleme_hairstyles
```

### 2. Install Dependencies

```bash
cd hairstyle_collector
npm install
```

### 3. Run Development Server

```bash
npx vite --port 8080
```

Access the application at: `http://localhost:8080`

---

## Directory Structure

```
hairstyle_collector/
├── .env.example
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── App.vue
    ├── main.js
    ├── components/
    │   ├── ImageModal.vue
    │   ├── Navbar.vue
    │   ├── SavingModal.vue
    │   └── Toast.vue
    ├── router/
    │   └── index.js
    ├── services/
    │   ├── cloudinary.js
    │   ├── config.js
    │   └── firebase.js
    └── views/
        ├── CatalogView.vue
        ├── FormView.vue
        └── NotFoundView.vue
```

---

## Database Schema (Firestore)

Each document in the `hairstyles` collection contains the following fields:

- `status`: String (`"main_page"` | `"draft"`)
- `name`: String (Hairstyle Title)
- `slug`: String (Unique URL Key)
- `variation_name`: String (Cut Variation)
- `faceshape`: String (`"oval"`, `"round"`, `"square"`, `"heart"`, `"diamond"`, `"oblong"`)
- `gender`: String (`"male"`, `"female"`)
- `tagline`: String (Short Catchphrase)
- `shape_badge`: String (Badge Text)
- `score_badge`: String (Match Score Text)
- `hair_length`: String
- `hair_texture`: String
- `styling_time`: String
- `maintenance`: String
- `main_img`: String (Cloudinary CDN URL)
- `description`: String (Full Description)
- `reasons`: Array of Strings (Recommendation Checklist)
- `tips`: Array of Strings (Care & Styling Tips)
- `suitability`: Array of Objects (`{ shape, score }`)
- `angles`: Array of Objects (`{ name, img }`)
- `created_at`: String (ISO Timestamp)
