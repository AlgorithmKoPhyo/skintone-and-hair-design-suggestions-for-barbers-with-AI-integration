<template>
  <section class="not-found-container">
    <div class="not-found-card">
      <div class="not-found-icon">
        <i class="fa-solid fa-triangle-exclamation"></i>
      </div>
      <h1 class="error-code">404</h1>
      <h2>Page Not Found</h2>
      <p>The page or route you are looking for does not exist or has been moved.</p>
      
      <router-link to="/catalog" class="btn btn-primary btn-home">
        <i class="fa-solid fa-house"></i> Back to Data Catalog
      </router-link>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 1.5rem;
  animation: fadeIn 0.3s ease;
}

.not-found-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 3.5rem 2.5rem;
  text-align: center;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
}

.not-found-icon {
  font-size: 3.5rem;
  color: #f59e0b;
  margin-bottom: 1rem;
}

.error-code {
  font-size: 4rem;
  font-weight: 800;
  color: #6366f1;
  line-height: 1;
  font-family: 'Outfit', sans-serif;
}

.not-found-card h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0.5rem 0;
}

.not-found-card p {
  color: #64748b;
  font-size: 0.92rem;
  margin-bottom: 2rem;
}

.btn-home {
  padding: 0.75rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 700;
}
</style>
