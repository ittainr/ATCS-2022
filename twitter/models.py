"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.follower_id",
                             secondaryjoin="User.username==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.following_id",
                             secondaryjoin="User.username==Follower.follower_id",
                             overlaps="following")
    
    tweets=relationship("Tweet", back_populates="user")

    def __repr__(self):
        return f"@{self.username}"


class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))

class Tweet(Base):
    __tablename__="tweets"

    #Columns
    id = Column("id", INTEGER, primary_key=True)
    content=Column("content", TEXT, nullable=False)
    timestamp=Column("timestamp", DATETIME, nullable=False)
    username=Column("username", TEXT, ForeignKey('users.username'))
    tags=relationship("Tag", secondary="tweettags", back_populates="tweets")
    user=relationship("User", back_populates="tweets")

    def __repr__(self):
        return f"{self.user}\n{self.content}\n{' '.join(map(str, self.tags))}\n{self.timestamp}"

class Tag(Base):
    __tablename__="tags"

    #Columns
    id = Column("id", INTEGER, primary_key=True)
    content=Column("content", TEXT, nullable=False)
    tweets=relationship("Tweet", secondary="tweettags", back_populates="tags")

    def __repr__(self):
        return f"#{self.content}"

class TweetTag(Base):
    __tablename__="tweettags"

    #Columns
    id = Column("id", INTEGER, primary_key=True)
    tweet_id=Column("tweet_id", INTEGER, ForeignKey("tweets.id"))
    tag_id=Column("tag_id", INTEGER, ForeignKey("tags.id"))
