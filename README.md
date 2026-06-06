# Simple Blog App

<p align="center">
  <img src="assets/github-social-preview.png" alt="Simple Blog App" width="100%" />
</p>

A full-stack blogging application where users can write, read, like, and comment on blogs.

**Stack:** Flask · SQLite · Vue 3 (Vite)

---

## Project Structure

```
simple-blog-app/
├── backend/
│   └── routes/
└── frontend/
    └── src/
        ├── components/
        ├── composables/
        ├── router/
        ├── utils/
        └── views/
```

---

## Routes

| Path               | View           | Description                       |
| ------------------ | -------------- | --------------------------------- |
| `/`                | `LoginView`    | Login page                        |
| `/register`        | `RegisterView` | Registration page                 |
| `/feed`            | `FeedView`     | All blogs, newest first           |
| `/write`           | `WriteView`    | Compose a new blog                |
| `/blog/:slug`      | `BlogView`     | Full blog with likes and comments |
| `/profile/:userId` | `ProfileView`  | All blogs by a user               |

### API endpoints

#### Auth
| Method   | URL                          | Description              |
| -------- | ---------------------------- | ------------------------ |
| `POST`   | `/api/register`              | Create account           |
| `POST`   | `/api/login`                 | Log in                   |
| `POST`   | `/api/logout`                | Log out                  |
| `GET`    | `/api/whoami`                | Current user info        |

#### Blogs
| Method   | URL                          | Description              |
| -------- | ---------------------------- | ------------------------ |
| `GET`    | `/api/blogs`                 | List all blogs           |
| `POST`   | `/api/blogs`                 | Create a blog            |
| `GET`    | `/api/blogs/<slug>`          | Get a blog with comments |
| `GET`    | `/api/users/<id>/blogs`      | Get all blogs by a user  |

#### Interactions
| Method   | URL                          | Description              |
| -------- | ---------------------------- | ------------------------ |
| `POST`   | `/api/blogs/<slug>/like`     | Toggle like              |
| `POST`   | `/api/blogs/<slug>/comments` | Add a comment            |
| `DELETE` | `/api/comments/<id>`         | Delete a comment         |

---

## Running the Application

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Runs on `http://localhost:5000`. On first run, creates the database and seeds demo data.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:5173`.

---

## Screenshots

Path: `/feed` — Global Feed
<img src="assets/feed_page.png" alt="Global Feed" width="100%" />

Path: `/write` — Write Blog
<img src="assets/write_page.png" alt="Write Blog" width="100%" />

Path: `/blog/:slug` — Blog View
<img src="assets/blog_page.png" alt="Blog View" width="100%" />

Path: `/profile/:userId` — User Profile
<img src="assets/profile_page.png" alt="User Profile" width="100%" />

Path: `/` — Login Page
<img src="assets/login_page.png" alt="Login Page" width="100%" />
