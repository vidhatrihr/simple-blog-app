from werkzeug.security import generate_password_hash
from models import db, User, Blog, Comment, Like
from datetime import datetime, timezone


def populate_db():
    if User.query.count() > 0:
        return

    # create demo users
    vidhatri = User(
        name='Vidhatri',
        email='vidhatri@example.com',
        password=generate_password_hash('password123')
    )
    vishnu = User(
        name='Vishnu',
        email='vishnu@example.com',
        password=generate_password_hash('password123')
    )
    db.session.add_all([vidhatri, vishnu])
    db.session.flush()

    # create sample blogs
    blog1 = Blog(
        title='Getting Started with Vue 3',
        slug='getting-started-with-vue-3',
        description='A beginner-friendly introduction to Vue 3 and the Composition API.',
        content='''Vue 3 is a progressive JavaScript framework for building user interfaces. It is designed from the ground up to be incrementally adoptable.

The Composition API is one of the biggest additions in Vue 3. Instead of using the Options API (data, methods, computed as separate object keys), you write all your logic inside a single setup() function — or more conveniently with the script setup syntax.

Here is why beginners should start with Vue 3:

1. Simple and readable syntax
2. Great documentation on vuejs.org
3. Vite as the build tool makes hot reload blazing fast
4. The ecosystem around it (Vue Router, Pinia) is clean and well-maintained

To get started, just run: npm create vite@latest my-app -- --template vue

That creates a fresh project in seconds. From there, open App.vue and start building.''',
        user_id=vidhatri.id
    )
    blog2 = Blog(
        title='Why SQLite is Perfect for Learning',
        slug='why-sqlite-is-perfect-for-learning',
        description='SQLite requires zero setup. Here is why it is the best database to learn on.',
        content='''When you are learning backend development, the last thing you want is to spend an hour setting up a database server. SQLite solves that.

SQLite is a serverless database. There is no daemon to start, no port to configure, no credentials to manage. The entire database is a single file on disk.

With Flask and SQLAlchemy, you connect to it with one line:
SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

That is it. SQLAlchemy creates the file automatically on first run.

For learning projects, SQLite is good enough. You get full SQL support, foreign keys, indexes, transactions — everything you need to understand how relational databases work.

When you eventually move to production, switching to PostgreSQL is mostly a config change. The SQLAlchemy models stay the same.

So for learners: ignore PostgreSQL for now. Start with SQLite. Get your app working. Learn the concepts. Scale later.''',
        user_id=vishnu.id
    )
    blog3 = Blog(
        title='Flask in Five Minutes',
        slug='flask-in-five-minutes',
        description='The absolute minimum you need to know to build a Flask REST API.',
        content='''Flask is a micro web framework for Python. Micro does not mean it lacks features — it means it gives you the minimum and lets you add what you need.

A basic Flask app looks like this:

from flask import Flask
app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello, World!'

That is a working web server. Run it with python app.py and visit http://localhost:5000/hello in your browser.

For a REST API, you return JSON instead of plain text. Flask makes this easy with the jsonify() function.

Flask also integrates well with extensions:
- flask-sqlalchemy for database access
- flask-login for session management
- flask-cors for cross-origin requests from your frontend

These three extensions, combined with Flask itself, are enough to build a full authentication system and data API. That is exactly what this blog app uses.''',
        user_id=vidhatri.id
    )
    db.session.add_all([blog1, blog2, blog3])
    db.session.flush()

    # seed likes
    like1 = Like(user_id=vishnu.id, blog_id=blog1.id)
    like2 = Like(user_id=vidhatri.id, blog_id=blog2.id)
    like3 = Like(user_id=vidhatri.id, blog_id=blog3.id)
    db.session.add_all([like1, like2, like3])

    # seed comments
    comment1 = Comment(content='Great intro! This helped me understand the Composition API.', user_id=vishnu.id, blog_id=blog1.id)
    comment2 = Comment(content='I had no idea SQLite was this simple to set up. Thanks!', user_id=vidhatri.id, blog_id=blog2.id)
    comment3 = Comment(content='Flask really is that simple. Loved this overview.', user_id=vishnu.id, blog_id=blog3.id)
    db.session.add_all([comment1, comment2, comment3])

    db.session.commit()
    print('Database seeded — login: vidhatri@example.com / password123')
