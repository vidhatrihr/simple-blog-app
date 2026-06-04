<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiRequest } from '@/utils/api.js'

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

async function register() {
  error.value = ''
  const res = await apiRequest('/register', {
    method: 'POST',
    body: { name: name.value, email: email.value, password: password.value },
  })
  const json = await res.json()
  if (!res.ok) {
    error.value = json.message
    return
  }
  router.push('/feed')
}
</script>

<template>
  <div class="page-center">
    <div class="card">
      <h1>Create account</h1>
      <p class="sub">Join and start writing today</p>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="name">Name</label>
          <input id="name" v-model="name" type="text" placeholder="Your name" required />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" v-model="email" type="email" placeholder="you@example.com" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" placeholder="••••••••" required />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button id="register-btn" type="submit" class="btn-primary submit-btn">Create account</button>
      </form>
      <p class="auth-footer">
        Already have an account?
        <RouterLink to="/" class="link">Sign in</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
.submit-btn {
  margin-top: 0.5rem;
}

.auth-footer {
  margin-top: 1.5rem;
  font-size: 0.88rem;
  color: var(--text-muted);
  text-align: center;
}
</style>
