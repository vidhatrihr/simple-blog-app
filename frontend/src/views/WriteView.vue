<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

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
    <NavBar>
      <button id="cancel-write-btn" class="btn-secondary" @click="router.push('/feed')">Cancel</button>
    </NavBar>

    <div class="write-header">
      <h1>Write a blog</h1>
      <button id="publish-btn" class="btn-primary publish-btn" @click="publish">Publish</button>
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
      <textarea id="blog-content" v-model="content" class="content-area" placeholder="Write your blog here..."></textarea>
    </div>
    <p v-if="error" class="error-msg">{{ error }}</p>
  </div>
</template>

<style scoped>
.write-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.write-header h1 {
  font-size: 1.3rem;
  font-weight: 600;
}

.publish-btn {
  width: auto;
  padding: 0.6rem 1.5rem;
}

.content-area {
  min-height: 360px;
}
</style>
