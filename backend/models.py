from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()


class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  email = Column(String, unique=True)
  password = Column(String)

  blogs = relationship('Blog', back_populates='author', cascade='all, delete-orphan')
  likes = relationship('Like', back_populates='user', cascade='all, delete-orphan')
  comments = relationship('Comment', back_populates='user', cascade='all, delete-orphan')


class Blog(db.Model):
  __tablename__ = 'blogs'
  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String, nullable=False)
  slug = Column(String, unique=True, nullable=False)
  description = Column(String)
  content = Column(Text)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(
      timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  user_id = Column(Integer, ForeignKey('users.id'))

  author = relationship('User', back_populates='blogs')
  likes = relationship('Like', back_populates='blog', cascade='all, delete-orphan')
  comments = relationship('Comment', back_populates='blog', cascade='all, delete-orphan')


class Like(db.Model):
  __tablename__ = 'likes'
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('users.id'))
  blog_id = Column(Integer, ForeignKey('blogs.id'))

  user = relationship('User', back_populates='likes')
  blog = relationship('Blog', back_populates='likes')


class Comment(db.Model):
  __tablename__ = 'comments'
  id = Column(Integer, primary_key=True, autoincrement=True)
  content = Column(Text, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  user_id = Column(Integer, ForeignKey('users.id'))
  blog_id = Column(Integer, ForeignKey('blogs.id'))

  user = relationship('User', back_populates='comments')
  blog = relationship('Blog', back_populates='comments')
