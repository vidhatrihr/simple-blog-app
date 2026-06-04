<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

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
  // Place new comment at top so it appears first
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
    <NavBar>
      <button id="back-to-feed-btn" class="btn-secondary" @click="router.push('/feed')">← Feed</button>
    </NavBar>

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

      <!-- Like bar -->
      <div class="like-bar">
        <button
          id="like-btn"
          class="like-btn"
          :class="{ liked: blog.liked }"
          @click="toggleLike"
        >
          {{ blog.liked ? '♥' : '♡' }} {{ blog.like_count }} {{ blog.like_count === 1 ? 'like' : 'likes' }}
        </button>
        <span class="comment-count">
          {{ blog.comment_count }} {{ blog.comment_count === 1 ? 'comment' : 'comments' }}
        </span>
      </div>

      <!-- Comments -->
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

        <div v-if="blog.comments.length === 0" class="empty comments-empty">
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
                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
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

<style scoped>
.blog-detail {
  padding-top: 1rem;
}

.blog-detail h1 {
  font-size: 1.8rem;
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 0.5rem;
}

.blog-detail .blog-desc {
  color: var(--text-muted);
  font-size: 1rem;
  margin-bottom: 1.25rem;
}

.blog-content {
  white-space: pre-wrap;
  line-height: 1.8;
  color: var(--text);
  margin: 2rem 0;
  border-top: 1px solid var(--border);
  padding-top: 2rem;
}

.like-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  margin-bottom: 2rem;
}

.like-btn {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-muted);
  cursor: pointer;
  font-family: inherit;
  font-size: 0.9rem;
  padding: 0.45rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: border-color 0.15s, color 0.15s;
}

.like-btn.liked {
  border-color: var(--accent);
  color: var(--accent);
}

.like-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.comment-count {
  color: var(--text-muted);
  font-size: 0.88rem;
}

.comments-section h2 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.comment-form {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.comment-form textarea {
  min-height: 70px;
  flex: 1;
}

.comment-form .btn-primary {
  width: auto;
  white-space: nowrap;
  align-self: flex-end;
}

.comments-empty {
  padding: 1.5rem 0;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-item {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem;
}

.comment-item.mine {
  border-color: var(--accent);
  border-opacity: 0.4;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--accent);
  cursor: pointer;
}

.comment-author:hover {
  text-decoration: underline;
}

.comment-date {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-left: 0.6rem;
}

.comment-content {
  font-size: 0.9rem;
  color: var(--text);
}

@media (max-width: 600px) {
  .comment-form {
    flex-direction: column;
  }

  .comment-form .btn-primary {
    width: 100%;
  }
}
</style>
