from werkzeug.security import generate_password_hash
from models import db, User, Blog, Comment, Like
import json


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

  # load sample blogs from JSON
  json_path = 'sample_blogs.json'
  with open(json_path, 'r', encoding='utf-8') as f:
    blogs_data = json.load(f)

  user_map = {
      'vidhatri@example.com': vidhatri,
      'vishnu@example.com': vishnu
  }

  blogs = []
  blog_map = {}
  for item in blogs_data:
    blog = Blog(
        title=item['title'],
        slug=item['slug'],
        description=item['description'],
        content=item['content'],
        user_id=user_map[item['author_email']].id
    )
    blogs.append(blog)
    blog_map[item['slug']] = blog

  db.session.add_all(blogs)
  db.session.flush()

  # seed likes
  like1 = Like(user_id=vishnu.id, blog_id=blog_map['getting-started-with-vue-3'].id)
  like2 = Like(user_id=vidhatri.id, blog_id=blog_map['why-sqlite-is-perfect-for-learning'].id)
  like3 = Like(user_id=vidhatri.id, blog_id=blog_map['flask-in-five-minutes'].id)
  db.session.add_all([like1, like2, like3])

  # seed comments
  comments = []
  for item in blogs_data:
    blog = blog_map[item['slug']]
    for comment_item in item.get('comments', []):
      comment = Comment(
          content=comment_item['content'],
          user_id=user_map[comment_item['user_email']].id,
          blog_id=blog.id
      )
      comments.append(comment)
  db.session.add_all(comments)

  db.session.commit()
  print('Database seeded - login: vidhatri@example.com / password123')
