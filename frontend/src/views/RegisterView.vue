<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

async function register() {
  error.value = ''
  const res = await fetch('http://localhost:5000/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ name: name.value, email: email.value, password: password.value }),
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
        <button id="register-btn" type="submit" class="btn-primary" style="margin-top: 0.5rem">Create account</button>
      </form>
      <p style="margin-top: 1.5rem; font-size: 0.88rem; color: var(--text-muted); text-align: center">
        Already have an account?
        <RouterLink to="/" class="link">Sign in</RouterLink>
      </p>
    </div>
  </div>
</template>
