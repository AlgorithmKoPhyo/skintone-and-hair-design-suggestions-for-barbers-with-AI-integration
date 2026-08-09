/* ==========================================================================
   StyleMe Data Collector - Configuration Module (Vite .env Variables)
   ========================================================================== */

export const config = {
  // Cloudinary Credentials (loaded from .env VITE_CLOUDINARY_*)
  cloudinary: {
    cloudName: (import.meta.env.VITE_CLOUDINARY_CLOUD_NAME || "").replace(/"/g, '').trim(),
    uploadPreset: (import.meta.env.VITE_CLOUDINARY_UPLOAD_PRESET || "").replace(/"/g, '').trim(),
    apiKey: (import.meta.env.VITE_CLOUDINARY_API_KEY || "").replace(/"/g, '').trim()
  },

  // Firebase Firestore Credentials (loaded from .env VITE_FIREBASE_*)
  firebase: {
    apiKey: (import.meta.env.VITE_FIREBASE_API_KEY || "").replace(/"/g, '').trim(),
    authDomain: (import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "").replace(/"/g, '').trim(),
    projectId: (import.meta.env.VITE_FIREBASE_PROJECT_ID || "").replace(/"/g, '').trim(),
    storageBucket: (import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "").replace(/"/g, '').trim(),
    messagingSenderId: (import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "").replace(/"/g, '').trim(),
    appId: (import.meta.env.VITE_FIREBASE_APP_ID || "").replace(/"/g, '').trim(),
    measurementId: (import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || "").replace(/"/g, '').trim()
  }
};
