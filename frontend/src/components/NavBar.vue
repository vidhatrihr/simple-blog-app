<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <nav class="nav">
    <span class="nav-brand" @click="router.push('/feed')">Simple Blog</span>
    <div class="nav-actions">
      <slot />
    </div>
  </nav>
</template>
