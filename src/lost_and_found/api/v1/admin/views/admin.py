from sqladmin import ModelView

from src.lost_and_found.adapters.orm import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.posts, User.comments]