<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const API = 'http://localhost:5000/api'
const opts = { credentials: 'include' }

const profileName = ref('')
const blogs = ref([])

onMounted(async () => {
  const meRes = await fetch(`${API}/me`, opts)
  if (!meRes.ok) {
    router.push('/')
    return
  }

  const blogsRes = await fetch(`${API}/users/${route.params.userId}/blogs`, opts)
  const blogsJson = await blogsRes.json()
  blogs.value = blogsJson.data
  if (blogs.value.length > 0) profileName.value = blogs.value[0].author.name
})

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
  <div class="app-layout">
    <nav class="nav">
      <span class="nav-brand" style="cursor:pointer" @click="router.push('/feed')">Simple Blog</span>
      <div class="nav-actions">
        <button id="back-to-feed-profile-btn" class="btn-secondary" @click="router.push('/feed')">← Feed</button>
      </div>
    </nav>

    <div class="profile-header">
      <h1>{{ profileName || 'Profile' }}</h1>
      <p>{{ blogs.length }} {{ blogs.length === 1 ? 'blog' : 'blogs' }} published</p>
    </div>

    <div v-if="blogs.length === 0" class="empty">This user hasn't written anything yet.</div>

    <div class="feed">
      <div
        v-for="blog in blogs"
        :key="blog.id"
        class="blog-card"
        @click="router.push(`/blog/${blog.slug}`)"
      >
        <h2>{{ blog.title }}</h2>
        <p class="description">{{ blog.description }}</p>
        <div class="blog-meta">
          <span>{{ formatDate(blog.created_at) }}</span>
          <span class="meta-dot">·</span>
          <span>{{ blog.like_count }} {{ blog.like_count === 1 ? 'like' : 'likes' }}</span>
          <span class="meta-dot">·</span>
          <span>{{ blog.comment_count }} {{ blog.comment_count === 1 ? 'comment' : 'comments' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
