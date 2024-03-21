from sqladmin import ModelView

from src.lost_and_found.adapters.orm import User, FeedbackMessage, Comment, Post


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.posts, User.comments, User.session_uuid]


class FeedbackMessageAdmin(ModelView, model=FeedbackMessage):
    column_list = [FeedbackMessage.id, FeedbackMessage.email, FeedbackMessage.text, FeedbackMessage.date]


class CommentAdmin(ModelView, model=Comment):
    column_list = [Comment.id, Comment.text, Comment.date, Comment.author, Comment.post]


class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.name, Post.date, Post.comments, Post.author, Post.photo, Post.description]