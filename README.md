# Simple Blog App — Project Report

**Stack:** Flask (Python) · SQLite · Vue 3 (Vite) · Pure CSS  
**Demo credentials:** `vidhatri@example.com` / `password123`

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Structure](#2-project-structure)
3. [Backend](#3-backend)
   - 3.1 [Dependencies](#31-dependencies)
   - 3.2 [app.py — Entry Point](#32-apppy--entry-point)
   - 3.3 [models.py — Database Models](#33-modelspy--database-models)
   - 3.4 [populate_db.py — Seed Data](#34-populate_dbpy--seed-data)
   - 3.5 [routes/auth.py — Auth Blueprint](#35-routesauthpy--auth-blueprint)
   - 3.6 [routes/blogs.py — Blogs Blueprint](#36-routesblogspy--blogs-blueprint)
4. [Frontend](#4-frontend)
   - 4.1 [index.html](#41-indexhtml)
   - 4.2 [main.js](#42-mainjs)
   - 4.3 [App.vue](#43-appvue)
   - 4.4 [router/index.js — Client-Side Routing](#44-routerindexjs--client-side-routing)
   - 4.5 [style.css — Global Styles](#45-stylecss--global-styles)
   - 4.6 [LoginView.vue](#46-loginviewvue)
   - 4.7 [RegisterView.vue](#47-registerviewvue)
   - 4.8 [FeedView.vue](#48-feedviewvue)
   - 4.9 [WriteView.vue](#49-writeviewvue)
   - 4.10 [BlogView.vue](#410-blogviewvue)
   - 4.11 [ProfileView.vue](#411-profileviewvue)
5. [Business Logic & Data Flow](#5-business-logic--data-flow)
6. [API Reference](#6-api-reference)
7. [Running the Application](#7-running-the-application)

---

## 1. Project Overview

The Simple Blog App is a web application where users can:

- Create an account and log in
- Write and publish blogs with a title, description, and full content
- Browse a feed of all blogs in reverse-chronological order (newest first)
- Read any blog's full content on a dedicated page
- Like a blog (toggleable — like and unlike)
- Leave comments on a blog
- Delete their own comments
- View a user's profile page showing all blogs they've written
- Log out

This is a beginner-targeted project. The code is intentionally simple, readable, and direct.

---

## 2. Project Structure

```
simple-blog-app/
├── AGENTS.md                        # architecture and coding guidelines
├── PROJECT_IDEA.md                  # project requirements
├── backend/
│   ├── app.py                       # Flask app — config, db, blueprints
│   ├── models.py                    # database tables as Python classes
│   ├── populate_db.py               # seed function — demo data
│   ├── requirements.txt             # pip packages
│   ├── blog.db                      # SQLite database (auto-created)
│   └── routes/
│       ├── __init__.py              # makes routes/ a Python package
│       ├── auth.py                  # register, login, logout, whoami
│       └── blogs.py                 # blog, like, comment endpoints
└── frontend/
    ├── index.html                   # HTML shell
    └── src/
        ├── main.js                  # creates Vue app, mounts it
        ├── style.css                # all CSS — global and component styles
        ├── App.vue                  # root Vue component
        ├── router/
        │   └── index.js             # URL → component mapping
        └── views/
            ├── LoginView.vue        # /  — login page
            ├── RegisterView.vue     # /register — signup page
            ├── FeedView.vue         # /feed — main blog feed
            ├── WriteView.vue        # /write — compose a blog
            ├── BlogView.vue         # /blog/:slug — full blog + comments
            └── ProfileView.vue      # /profile/:userId — user's blogs
```

---

## 3. Backend

The backend is a Flask web server that exposes a REST API. It runs on port **5000**.

### 3.1 Dependencies

| Package | Purpose |
| --- | --- |
| `flask` | Web framework — handles HTTP routing |
| `flask-cors` | Allows the frontend (port 5173) to call the backend (port 5000) |
| `flask-login` | Manages user sessions — tracks who is logged in |
| `flask-sqlalchemy` | ORM — lets us write Python classes instead of raw SQL |
| `werkzeug` | Bundled with Flask — used for password hashing |

---

### 3.2 `app.py` — Entry Point

This is the first file Flask runs. It wires everything together.

**What it does, step by step:**

1. **Creates the Flask app** and sets a `secret_key`. The secret key signs session cookies.
2. **Configures session cookies** for cross-site requests with `SameSite=None`, `Secure=True`, `HttpOnly=True`.
3. **Sets the database URI** to `sqlite:///blog.db`. SQLite creates this file automatically.
4. **Configures CORS** with `supports_credentials=True`, restricted to `http://localhost:5173`.
5. **Initialises Flask-SQLAlchemy** by calling `db.init_app(app)`.
6. **Configures Flask-Login** with a `LoginManager` and `load_user` callback.
7. **Registers both blueprints** (`auth_bp`, `blogs_bp`) under the `/api` prefix.
8. **Inside `app_context()`**: creates all DB tables, then calls `populate_db()`.
9. **Starts the server** on port 5000 in debug mode.

---

### 3.3 `models.py` — Database Models

#### `User` table (`users`)

| Column | Type | Details |
| --- | --- | --- |
| `id` | Integer | Primary key, auto-incremented |
| `name` | String | User's display name |
| `email` | String | Unique — no two users share an email |
| `password` | String | Stores a **hashed** password, never plain text |

Relationships: `blogs`, `likes`, `comments` (all with cascade delete so removing a user removes all their data).

#### `Blog` table (`blogs`)

| Column | Type | Details |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `title` | String | Blog title |
| `slug` | String | URL-safe kebab-case version of the title, unique |
| `description` | String | Short summary shown in feed cards |
| `content` | Text | Full blog body (plain text) |
| `created_at` | DateTime | Set on insert |
| `updated_at` | DateTime | Updates on every write |
| `user_id` | Integer | Foreign key → `users.id` |

Relationships: `author`, `likes`, `comments`.

#### `Like` table (`likes`)

A join table between users and blogs. One row = one user liking one blog.

| Column | Type | Details |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `user_id` | Integer | Foreign key → `users.id` |
| `blog_id` | Integer | Foreign key → `blogs.id` |

#### `Comment` table (`comments`)

| Column | Type | Details |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `content` | Text | Comment body |
| `created_at` | DateTime | Set on insert |
| `user_id` | Integer | Foreign key → `users.id` |
| `blog_id` | Integer | Foreign key → `blogs.id` |

---

### 3.4 `populate_db.py` — Seed Data

Defines a `populate_db()` function. Called from `app.py` on every startup. Returns immediately if users already exist.

**What it seeds on a fresh database:**

1. Two users: **Vidhatri** (`vidhatri@example.com`) and **Rahul** (`rahul@example.com`), both with `password123`.
2. Three sample blogs spanning Flask, Vue 3, and SQLite topics.
3. Sample likes and comments so the feed is interactive from the first run.

---

### 3.5 `routes/auth.py` — Auth Blueprint

A Blueprint registered at `/api`. Provides four endpoints.

#### `POST /api/register`

1. Extract `name`, `email`, `password` from request JSON.
2. Check if email already exists — return `400` if so.
3. Create a `User` with `generate_password_hash(password)`.
4. Commit to DB, call `login_user(user)` — session cookie is set immediately.
5. Return `200`.

#### `POST /api/login`

1. Find user by email. If not found, return `401`.
2. `check_password_hash(user.password, plain_password)` — if mismatch, return `401`.
3. Call `login_user(user)`.
4. Return `200` with `{ name, email }`.

#### `POST /api/logout`

Calls `logout_user()`. Returns `200`.

#### `GET /api/whoami`

Returns `{ id, name, email }` for the currently logged-in user. Returns `401` if not logged in. Used by every page as an auth guard on mount.

---

### 3.6 `routes/blogs.py` — Blogs Blueprint

All routes require `@login_required`.

#### Slug generation

`make_slug(title)` converts a title to URL-safe kebab-case (lowercase, spaces to hyphens, special chars stripped). `unique_slug(base_slug)` appends a numeric suffix if the slug is already taken: `my-title`, `my-title-1`, `my-title-2`.

#### `serialize_blog(blog, current_user_id)`

Converts a `Blog` SQLAlchemy object to a plain dictionary safe to return as JSON. Includes `liked` boolean (whether the current user has liked it) and `like_count`, `comment_count`.

#### `GET /api/blogs`

Returns all blogs ordered by `created_at` descending (newest first). Serialised using `serialize_blog`.

#### `GET /api/blogs/<slug>`

Returns the full blog including `content` and all comments. Comments are sorted with the current user's comments first (newest), then others' (newest). Each comment includes `is_mine: true/false`.

#### `POST /api/blogs`

Creates a new blog. Generates and ensures a unique slug from the title. Returns the serialised new blog.

#### `GET /api/users/<user_id>/blogs`

Returns all blogs by a specific user, newest first. Used by the profile page.

#### `POST /api/blogs/<slug>/like`

Toggles the like for the current user. If a `Like` row exists, deletes it (unlike). If not, creates it (like). Returns `{ liked, like_count }`.

#### `POST /api/blogs/<slug>/comments`

Creates a new comment on the blog. Returns the new comment object with `is_mine: true`.

#### `DELETE /api/comments/<comment_id>`

Deletes a comment. Returns `403` if the comment does not belong to the current user.

---

## 4. Frontend

A Vue 3 SPA. The browser loads the app once and Vue Router handles all navigation without page reloads. Runs on port **5173**.

### 4.1 `index.html`

The single HTML shell. Contains the Inter font from Google Fonts, a meta description for SEO, and the `<div id="app">` mount point.

---

### 4.2 `main.js`

Creates the Vue app, installs Vue Router, imports `style.css`, and mounts to `#app`.

---

### 4.3 `App.vue`

A thin wrapper. Contains only `<RouterView />`. No logic.

---

### 4.4 `router/index.js` — Client-Side Routing

| Path | View | Notes |
| --- | --- | --- |
| `/` | `LoginView.vue` | Default route |
| `/register` | `RegisterView.vue` | Signup page |
| `/feed` | `FeedView.vue` | Main app — blog list |
| `/write` | `WriteView.vue` | Compose a blog |
| `/blog/:slug` | `BlogView.vue` | Full blog + comments |
| `/profile/:userId` | `ProfileView.vue` | User's published blogs |

`createWebHistory` gives clean URLs (no `#`).

---

### 4.5 `style.css` — Global Styles

All CSS lives in this single file.

#### Design Tokens (CSS Variables)

| Variable | Value | Usage |
| --- | --- | --- |
| `--bg` | `#0f0f11` | Page background |
| `--surface` | `#18181c` | Cards, nav surfaces |
| `--surface-alt` | `#222228` | Input backgrounds |
| `--border` | `#2e2e36` | All borders |
| `--accent` | `#c8f55a` | Primary action color (lime-green) |
| `--text` | `#e8e8ee` | Main text |
| `--text-muted` | `#7a7a8c` | Labels, secondary text |
| `--danger` | `#f55a5a` | Errors, delete buttons |
| `--radius` | `10px` | Card border radius |
| `--gap` | `1.5rem` | Standard spacing |

Variables are named by **context**, not by color — `--danger`, not `--red`.

#### Key Style Classes

| Class | What it styles |
| --- | --- |
| `.page-center` | Full-screen centering — login and register pages |
| `.card` | Auth form wrapper (dark, bordered) |
| `.form-group` | Label + input stacked vertically |
| `.btn-primary` | Lime-green full-width action button |
| `.btn-secondary` | Outlined neutral button — nav actions |
| `.btn-danger` | Outlined red button — delete actions |
| `.error-msg` | Red inline error text |
| `.app-layout` | Max-width centered container for all app pages |
| `.nav` | Top navigation bar — brand + actions |
| `.feed` | Vertical list of blog cards |
| `.blog-card` | Clickable card in the feed |
| `.blog-detail` | Full blog page layout |
| `.like-bar` | Like button + comment count row |
| `.comments-section` | Comment form + comment list |
| `.comment-item` | Individual comment card |
| `.comment-item.mine` | Accent-bordered highlight for own comments |
| `.profile-header` | Author name + blog count header |
| `.empty` | Centered muted text — empty states |

---

### 4.6 `LoginView.vue`

**Route:** `/`

**State:** `email`, `password`, `error`

**`login()` function:**
1. Clears any previous error.
2. Sends `POST /api/login` with `credentials: 'include'`.
3. On failure: sets `error.value` from the server message.
4. On success: `router.push('/feed')`.

---

### 4.7 `RegisterView.vue`

**Route:** `/register`

**State:** `name`, `email`, `password`, `error`

**`register()` function:**
1. Sends `POST /api/register`.
2. On failure: shows inline error.
3. On success: redirects to `/feed` — the backend has already logged the user in.

---

### 4.8 `FeedView.vue`

**Route:** `/feed`

**State:** `user`, `blogs`

**`onMounted()`:**
1. `GET /api/whoami` — if `401`, redirect to `/`. Sets `user.value`.
2. `GET /api/blogs` — loads all blogs, newest first.

**Template:** Nav bar with user name, Write button, Sign out button. A list of `.blog-card` elements. Each card shows title, description, author (clickable → profile), date, like count, comment count. Clicking the card navigates to `/blog/:slug`.

---

### 4.9 `WriteView.vue`

**Route:** `/write`

**State:** `title`, `description`, `content`, `error`

**`onMounted()`:** Checks session via `GET /api/whoami`. Redirects to `/` if unauthenticated.

**`publish()` function:**
1. Validates title and content are not empty.
2. Sends `POST /api/blogs` with title, description, content.
3. On success: redirects to `/blog/:slug` of the newly created blog.

---

### 4.10 `BlogView.vue`

**Route:** `/blog/:slug`

**State:** `blog` (includes `title`, `slug`, `description`, `content`, `author`, `like_count`, `liked`, `comment_count`, `comments`), `currentUserId`, `newComment`

**`onMounted()`:**
1. `GET /api/whoami` — auth guard, sets `currentUserId`.
2. `loadBlog()` — `GET /api/blogs/:slug`.

**`toggleLike()`:** `POST /api/blogs/:slug/like`. Updates `blog.liked` and `blog.like_count` from the response — no full reload.

**`addComment()`:** `POST /api/blogs/:slug/comments`. Prepends the new comment to the top of the list (it's the user's own comment, so it belongs at the top). Increments `comment_count`.

**`deleteComment(id)`:** `DELETE /api/comments/:id`. Filters the deleted comment out of `blog.comments`. Decrements `comment_count`.

**Template:**
- Blog title, description, meta row (author → profile, date)
- Full content in a `<pre>`-style block (preserves whitespace)
- Like bar with a toggle button (♡/♥) + comment count
- Comment form (textarea + Post button)
- Comment list — own comments are highlighted with the accent border and have a Delete button

---

### 4.11 `ProfileView.vue`

**Route:** `/profile/:userId`

**State:** `profileName`, `blogs`

**`onMounted()`:**
1. `GET /api/whoami` — auth guard.
2. `GET /api/users/:userId/blogs` — loads that user's blogs.
3. Sets `profileName` from the first blog's `author.name`.

**Template:** Author name heading, blog count, feed of blog cards (same card layout as `FeedView`). No author column since all blogs on the profile belong to the same person.

---

## 5. Business Logic & Data Flow

### Registration Flow

```
User fills form → POST /api/register
  → Server creates User (hashed password)
  → Server calls login_user() — session cookie set
  → 200 OK
  → Frontend redirects to /feed
```

### Login Flow

```
User fills form → POST /api/login
  → Server finds user by email
  → check_password_hash() verifies password
  → login_user() — session cookie set
  → 200 OK
  → Frontend redirects to /feed
```

### Feed Load Flow

```
Vue mounts FeedView
  → GET /api/whoami (verify session)
      → 401: redirect to /
      → 200: set user
  → GET /api/blogs → set blogs array
  → template renders feed cards
```

### Like Toggle Flow

```
User clicks like button → toggleLike()
  → POST /api/blogs/:slug/like
  → Server: find or delete Like row
  → 200 { liked, like_count }
  → Frontend updates blog.liked + blog.like_count in place
  → Button text and style update reactively
```

### Comment Add Flow

```
User types comment → click Post → addComment()
  → POST /api/blogs/:slug/comments
  → Server creates Comment
  → 200 { comment object }
  → Frontend prepends comment to top of list
  → comment_count increments
```

### Comment Delete Flow

```
User clicks Delete → deleteComment(id)
  → DELETE /api/comments/:id
  → Server verifies ownership, deletes row
  → 200
  → Frontend filters comment out of list
  → comment_count decrements
```

### Session Persistence

The browser stores the session as a cookie. `credentials: 'include'` on every fetch ensures the cookie is sent automatically. Flask-Login reads the cookie and makes the user available as `current_user` on every request.

### Slug Generation

When a blog is published, the title is converted to a slug: lowercase, spaces to hyphens, special characters removed. `unique_slug()` checks the database and appends a counter if the slug already exists, ensuring every blog has a unique, shareable URL.

---

## 6. API Reference

All endpoints are prefixed with `/api`. Responses follow `{ "data": ..., "message": "..." }`.

| Method | URL | Auth | Request Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/api/register` | No | `{ name, email, password }` | `{ message }` |
| `POST` | `/api/login` | No | `{ email, password }` | `{ message, data: { name, email } }` |
| `POST` | `/api/logout` | Yes | — | `{ message }` |
| `GET` | `/api/whoami` | Yes | — | `{ data: { id, name, email } }` |
| `GET` | `/api/blogs` | Yes | — | `{ data: [ ...blogs ] }` |
| `GET` | `/api/blogs/<slug>` | Yes | — | `{ data: blog with content + comments }` |
| `POST` | `/api/blogs` | Yes | `{ title, description, content }` | `{ message, data: blog }` |
| `GET` | `/api/users/<id>/blogs` | Yes | — | `{ data: [ ...blogs ] }` |
| `POST` | `/api/blogs/<slug>/like` | Yes | — | `{ data: { liked, like_count } }` |
| `POST` | `/api/blogs/<slug>/comments` | Yes | `{ content }` | `{ message, data: comment }` |
| `DELETE` | `/api/comments/<id>` | Yes | — | `{ message }` |

**Auth = Yes** means the session cookie must be present. Without it, Flask-Login returns `401`.

---

## 7. Running the Application

### Start the Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

On first run:
- Creates `blog.db` in the `backend/` folder
- Creates all tables (`users`, `blogs`, `likes`, `comments`)
- Seeds the database with 2 demo users and 3 sample blogs
- Prints: `Database seeded — login: vidhatri@example.com / password123`
- Flask listens on `http://localhost:5000`

### Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite starts at `http://localhost:5173`.

Open `http://localhost:5173` in a browser. Use the demo credentials or register a new account.
