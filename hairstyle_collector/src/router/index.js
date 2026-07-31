/* ==========================================================================
   StyleMe Data Collector - Vue Router Setup (HTML5 Web History & 404 Catch-All)
   ========================================================================== */

import { createRouter, createWebHistory } from 'vue-router';
import CatalogView from '../views/CatalogView.vue';
import FormView from '../views/FormView.vue';
import NotFoundView from '../views/NotFoundView.vue';

const routes = [
  { path: '/', redirect: '/catalog' },
  { path: '/catalog', name: 'Catalog', component: CatalogView },
  { path: '/create', name: 'Create', component: FormView },
  { path: '/edit/:id', name: 'Edit', component: FormView },
  
  // 404 Catch-All Fallback Route
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
