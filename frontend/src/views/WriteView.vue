<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API = 'http://localhost:5000/api'
const opts = { credentials: 'include' }

const title = ref('')
const description = ref('')
const content = ref('')
const error = ref('')

onMounted(async () => {
  const res = await fetch(`${API}/whoami`, opts)
  if (!res.ok) router.push('/')
})

async function publish() {
  error.value = ''
  if (!title.value.trim() || !content.value.trim()) {
    error.value = 'Title and content are required.'
    return
  }
  const res = await fetch(`${API}/blogs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
      title: title.value.trim(),
      description: description.value.trim(),
      content: content.value.trim(),
    }),
  })
  const json = await res.json()
  if (!res.ok) {
    error.value = json.message
    return
  }
  router.push(`/blog/${json.data.slug}`)
}
</script>

<template>
  <div class="app-layout">
    <nav class="nav">
      <span class="nav-brand" style="cursor:pointer" @click="router.push('/feed')">Simple Blog</span>
      <div class="nav-actions">
        <button id="cancel-write-btn" class="btn-secondary" @click="router.push('/feed')">Cancel</button>
      </div>
    </nav>

    <div class="write-header">
      <h1>Write a blog</h1>
      <button id="publish-btn" class="btn-primary" style="width: auto; padding: 0.6rem 1.5rem" @click="publish">Publish</button>
    </div>

    <div class="form-group">
      <label for="blog-title">Title</label>
      <input id="blog-title" v-model="title" type="text" placeholder="Your blog title" />
    </div>
    <div class="form-group">
      <label for="blog-description">Description</label>
      <input id="blog-description" v-model="description" type="text" placeholder="A short summary (optional)" />
    </div>
    <div class="form-group">
      <label for="blog-content">Content</label>
      <textarea id="blog-content" v-model="content" style="min-height: 360px" placeholder="Write your blog here..."></textarea>
    </div>
    <p v-if="error" class="error-msg">{{ error }}</p>
  </div>
</template>
