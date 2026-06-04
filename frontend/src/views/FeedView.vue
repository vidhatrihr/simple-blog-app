<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API = 'http://localhost:5000/api'
const opts = { credentials: 'include' }

const user = ref(null)
const blogs = ref([])

onMounted(async () => {
  const meRes = await fetch(`${API}/whoami`, opts)
  if (!meRes.ok) {
    router.push('/')
    return
  }
  const meJson = await meRes.json()
  user.value = meJson.data

  const blogsRes = await fetch(`${API}/blogs`, opts)
  const blogsJson = await blogsRes.json()
  blogs.value = blogsJson.data
})

async function logout() {
  await fetch(`${API}/logout`, { method: 'POST', ...opts })
  router.push('/')
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
  <div class="app-layout">
    <nav class="nav">
      <span class="nav-brand" style="cursor:pointer" @click="router.push('/feed')">Simple Blog</span>
      <div class="nav-actions">
        <span
          v-if="user"
          id="my-profile-btn"
          style="color: var(--accent); font-size: 0.88rem; cursor: pointer"
          @click="router.push(`/profile/${user.id}`)"
        >{{ user.name }}</span>
        <button id="write-btn" class="btn-secondary" @click="router.push('/write')">Write</button>
        <button id="logout-btn" class="btn-secondary" @click="logout">Sign out</button>
      </div>
    </nav>

    <div v-if="blogs.length === 0" class="empty">No blogs yet. Be the first to write one.</div>

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
          <span
            class="author"
            @click.stop="router.push(`/profile/${blog.author.id}`)"
          >{{ blog.author.name }}</span>
          <span class="meta-dot">·</span>
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
