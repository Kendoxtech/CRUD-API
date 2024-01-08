from .db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(1000), nullable=False)
    published = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"),nullable=False)
    owner = relationship("User")
    votes = relationship("Vote")


class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True, nullable=False)
        email = Column(String, nullable=False, unique=True)
        password = Column(String, nullable=False)
        phone_number = Column(String)
        created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
      __tablename__ = "votes"
      user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
      post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True)