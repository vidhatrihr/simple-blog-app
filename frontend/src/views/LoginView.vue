<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API = 'http://localhost:5000/api'

const email = ref('')
const password = ref('')
const error = ref('')

async function login() {
  error.value = ''
  const res = await fetch(`${API}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ email: email.value, password: password.value }),
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
      <h1>Welcome back</h1>
      <p class="sub">Sign in to your account to continue</p>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" v-model="email" type="email" placeholder="you@example.com" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" placeholder="••••••••" required />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button id="login-btn" type="submit" class="btn-primary submit-btn">Sign in</button>
      </form>
      <p class="auth-footer">
        No account?
        <RouterLink to="/register" class="link">Create one</RouterLink>
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
