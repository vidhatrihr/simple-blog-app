# Simple Blog App

<p align="center">
  <img src="assets/screenshot-1.png" alt="Simple Blog App" width="75%" />
</p>

A full-stack blogging application where users can write, read, like, and comment on blogs.

**Stack:** Flask · SQLite · Vue 3 (Vite)

---

## Project Structure

```
simple-blog-app/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── populate_db.py
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py
│       └── blogs.py
└── frontend/
    └── src/
        ├── components/
        │   └── NavBar.vue
        ├── composables/
        │   └── useWhoAmI.js
        ├── utils/
        │   └── api.js
        ├── router/
        │   └── index.js
        ├── views/
        │   ├── LoginView.vue
        │   ├── RegisterView.vue
        │   ├── FeedView.vue
        │   ├── WriteView.vue
        │   ├── BlogView.vue
        │   └── ProfileView.vue
        ├── App.vue
        ├── main.js
        └── style.css
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

| Method   | URL                          | Description              |
| -------- | ---------------------------- | ------------------------ |
| `POST`   | `/api/register`              | Create account           |
| `POST`   | `/api/login`                 | Log in                   |
| `POST`   | `/api/logout`                | Log out                  |
| `GET`    | `/api/whoami`                | Current user info        |
| `GET`    | `/api/blogs`                 | List all blogs           |
| `POST`   | `/api/blogs`                 | Create a blog            |
| `GET`    | `/api/blogs/<slug>`          | Get a blog with comments |
| `GET`    | `/api/users/<id>/blogs`      | Get all blogs by a user  |
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

<table>
  <tr>
    <td><img src="assets/screenshot-1.png" alt="Screenshot 1" /></td>
    <td><img src="assets/screenshot-2.png" alt="Screenshot 2" /></td>
  </tr>
  <tr>
    <td><img src="assets/screenshot-3.png" alt="Screenshot 3" /></td>
    <td><img src="assets/screenshot-4.png" alt="Screenshot 4" /></td>
  </tr>
</table>
