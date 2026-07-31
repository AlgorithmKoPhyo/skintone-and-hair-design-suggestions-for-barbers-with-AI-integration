/* ==========================================================================
   StyleMe Data Collector - Firebase Firestore Database Service
   ========================================================================== */

import { initializeApp, getApps, getApp } from "firebase/app";
import { getFirestore, collection, addDoc, getDocs, doc, setDoc, deleteDoc } from "firebase/firestore";
import { config } from "./config.js";

let db = null;
let isConnected = false;

export function initFirestore() {
  const firebaseConfig = config.firebase;
  if (!firebaseConfig || !firebaseConfig.apiKey || !firebaseConfig.projectId) {
    isConnected = false;
    db = null;
    return false;
  }

  try {
    const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();
    db = getFirestore(app);
    isConnected = true;
    console.log("✓ Firebase Firestore connected!");
    return true;
  } catch (err) {
    console.error("Firestore init error:", err);
    isConnected = false;
    db = null;
    return false;
  }
}

export function isFirestoreReady() {
  return isConnected;
}

export async function saveToFirestore(record) {
  if (!isConnected || !db) throw new Error("Firestore is not connected.");
  const docRef = await addDoc(collection(db, "hairstyles"), record);
  return { success: true, id: docRef.id };
}

export async function updateInFirestore(id, record) {
  if (!isConnected || !db) throw new Error("Firestore is not connected.");
  const docRef = doc(db, "hairstyles", id);
  await setDoc(docRef, record, { merge: true });
  return { success: true, id };
}

export async function fetchFromFirestore() {
  if (!isConnected || !db) return [];
  const querySnapshot = await getDocs(collection(db, "hairstyles"));
  const items = [];
  querySnapshot.forEach((docSnap) => {
    items.push({ id: docSnap.id, ...docSnap.data() });
  });
  return items;
}

export async function deleteFromFirestore(id) {
  if (!isConnected || !db) throw new Error("Firestore is not connected.");
  await deleteDoc(doc(db, "hairstyles", id));
}
