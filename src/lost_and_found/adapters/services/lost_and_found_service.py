from src.notify.adapters.services.base import BaseService

from src.lost_and_found.adapters.orm import FeedbackMessage
from src.lost_and_found.adapters.repos.comment_repo import CommentRepo
from src.lost_and_found.adapters.repos.post_repo import PostRepo
from src.lost_and_found.adapters.repos.user_repo import UserRepo


class LostAndFoundService(BaseService):
    users_repo: UserRepo
    comment_repo: CommentRepo
    feedback_message: FeedbackMessage
    post_repo: PostRepo

    def __init__(self):
        self.users_repo = UserRepo()
        self.comment_repo = CommentRepo()
        self.feedback_message = FeedbackMessage()
        self.post_repo = PostRepo()
