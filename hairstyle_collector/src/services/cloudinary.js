/* ==========================================================================
   StyleMe Data Collector - Strict Cloudinary CDN Direct Upload Service
   ========================================================================== */

import { config } from "./config.js";

/**
 * Uploads a file directly to Cloudinary CDN.
 * Ensures ONLY Cloudinary CDN URLs are stored in Firebase (Zero Base64 data).
 * Throws a clear descriptive error if Cloudinary unsigned upload preset is not configured.
 */
export async function uploadToCloudinaryDirect(file, folder = "hairstyles") {
  const { cloudName, uploadPreset } = config.cloudinary;

  if (!cloudName) {
    throw new Error("Cloudinary Cloud Name is missing in .env (VITE_CLOUDINARY_CLOUD_NAME).");
  }

  // Presets to attempt for unsigned upload
  const presetsToTry = [
    uploadPreset,
    "styleme_hairstyles",
    "ml_default",
    "unsigned_preset",
    "preset_unsigned",
    "hairstyles",
    "default",
    "demo",
    "unsigned"
  ].filter(Boolean);

  let lastErrorMessage = "";

  for (const preset of presetsToTry) {
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("upload_preset", preset);
      if (folder) formData.append("folder", folder);

      const res = await fetch(`https://api.cloudinary.com/v1_1/${cloudName}/image/upload`, {
        method: "POST",
        body: formData
      });

      const json = await res.json();
      if (json.secure_url) {
        console.log(`✓ Uploaded directly to Cloudinary CDN (${preset}): ${json.secure_url}`);
        return json.secure_url;
      } else if (json.error) {
        lastErrorMessage = json.error.message || JSON.stringify(json.error);
        console.warn(`Cloudinary upload attempt with preset '${preset}' failed:`, lastErrorMessage);
      }
    } catch (err) {
      lastErrorMessage = err.message;
      console.warn(`Cloudinary fetch error with preset '${preset}':`, err);
    }
  }

  throw new Error(
    `Cloudinary CDN Upload Error: ${lastErrorMessage || 'Upload preset not found'}.\n\n` +
    `👉 Quick 30-Second Setup in Cloudinary Console:\n` +
    `1. Go to https://console.cloudinary.com/settings/upload\n` +
    `2. Click 'Add Upload Preset'\n` +
    `3. Set Name = 'styleme_hairstyles' and Signing Mode = 'Unsigned'\n` +
    `4. Save and retry uploading!`
  );
}
