<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const API = 'http://localhost:5000/api'
const opts = { credentials: 'include' }

const blog = ref(null)
const currentUserId = ref(null)
const newComment = ref('')

onMounted(async () => {
  const meRes = await fetch(`${API}/whoami`, opts)
  if (!meRes.ok) {
    router.push('/')
    return
  }
  const meJson = await meRes.json()
  currentUserId.value = meJson.data.id

  await loadBlog()
})

async function loadBlog() {
  const res = await fetch(`${API}/blogs/${route.params.slug}`, opts)
  if (!res.ok) {
    router.push('/feed')
    return
  }
  const json = await res.json()
  blog.value = json.data
}

async function toggleLike() {
  const res = await fetch(`${API}/blogs/${route.params.slug}/like`, {
    method: 'POST',
    credentials: 'include',
  })
  const json = await res.json()
  blog.value.liked = json.data.liked
  blog.value.like_count = json.data.like_count
}

async function addComment() {
  if (!newComment.value.trim()) return
  const res = await fetch(`${API}/blogs/${route.params.slug}/comments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ content: newComment.value.trim() }),
  })
  const json = await res.json()
  // add comment to top of list (mine shows first)
  blog.value.comments.unshift(json.data)
  blog.value.comment_count += 1
  newComment.value = ''
}

async function deleteComment(commentId) {
  await fetch(`${API}/comments/${commentId}`, {
    method: 'DELETE',
    credentials: 'include',
  })
  blog.value.comments = blog.value.comments.filter(c => c.id !== commentId)
  blog.value.comment_count -= 1
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
        <button id="back-to-feed-btn" class="btn-secondary" @click="router.push('/feed')">← Feed</button>
      </div>
    </nav>

    <div v-if="blog" class="blog-detail">
      <h1>{{ blog.title }}</h1>
      <p class="blog-desc">{{ blog.description }}</p>
      <div class="blog-meta">
        <span
          class="author"
          @click="router.push(`/profile/${blog.author.id}`)"
        >{{ blog.author.name }}</span>
        <span class="meta-dot">·</span>
        <span>{{ formatDate(blog.created_at) }}</span>
      </div>

      <div class="blog-content">{{ blog.content }}</div>

      <!-- like bar -->
      <div class="like-bar">
        <button
          id="like-btn"
          class="like-btn"
          :class="{ liked: blog.liked }"
          @click="toggleLike"
        >
          {{ blog.liked ? '♥' : '♡' }} {{ blog.like_count }} {{ blog.like_count === 1 ? 'like' : 'likes' }}
        </button>
        <span style="color: var(--text-muted); font-size: 0.88rem">
          {{ blog.comment_count }} {{ blog.comment_count === 1 ? 'comment' : 'comments' }}
        </span>
      </div>

      <!-- comments -->
      <div class="comments-section">
        <h2>Comments</h2>
        <div class="comment-form">
          <textarea
            id="comment-input"
            v-model="newComment"
            placeholder="Leave a comment..."
          ></textarea>
          <button id="add-comment-btn" class="btn-primary" @click="addComment">Post</button>
        </div>

        <div v-if="blog.comments.length === 0" class="empty" style="padding: 1.5rem 0">
          No comments yet. Be the first.
        </div>

        <div class="comment-list">
          <div
            v-for="comment in blog.comments"
            :key="comment.id"
            class="comment-item"
            :class="{ mine: comment.is_mine }"
          >
            <div class="comment-header">
              <div>
                <span
                  class="comment-author"
                  @click="router.push(`/profile/${comment.user.id}`)"
                >{{ comment.user.name }}</span>
                <span class="comment-date" style="margin-left: 0.6rem">{{ formatDate(comment.created_at) }}</span>
              </div>
              <button
                v-if="comment.is_mine"
                class="btn-danger"
                @click="deleteComment(comment.id)"
              >Delete</button>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
