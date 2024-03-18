import os
import uuid
from uuid import UUID

from fastapi import UploadFile
from fastapi.params import File
from sqlalchemy.ext.asyncio import AsyncSession

from src.lost_and_found.adapters.models.comment import CommentRetrieveModel, CommentCreateModel
from src.lost_and_found.adapters.models.feedback_message import (
    FeedbackMessageCreateModel,
)
from src.lost_and_found.adapters.models.post import PostRetrieveModel, PostCreateModel
from src.lost_and_found.adapters.models.user import UserCreateModel, UserRetrieveModel
from src.lost_and_found.adapters.repos.comment_repo import CommentRepo
from src.lost_and_found.adapters.repos.feedback_message_repo import FeedbackMessageRepo
from src.lost_and_found.adapters.repos.post_repo import PostRepo
from src.lost_and_found.adapters.repos.user_repo import UserRepo


class LostAndFoundService:
    users_repo: UserRepo
    comment_repo: CommentRepo
    feedback_message_repo: FeedbackMessageRepo
    post_repo: PostRepo

    def __init__(self):
        self.users_repo = UserRepo()
        self.comment_repo = CommentRepo()
        self.feedback_message_repo = FeedbackMessageRepo()
        self.post_repo = PostRepo()

    async def get_post_list(self, session: AsyncSession):
        return await self.post_repo.get_list(session=session)

    async def create_feedback_message(
        self, email: str, text: str, session: AsyncSession
    ):
        await self.feedback_message_repo.create(
            feedback_message=FeedbackMessageCreateModel(
                email=email,
                text=text,
            ),
            session=session,
        )

    async def register_user(self, password: str, username: str, session: AsyncSession):
        await self.users_repo.create_user(
            UserCreateModel(password=password, username=username), session=session
        )

    async def login_user(
        self, password: str, username: str, session: AsyncSession
    ) -> UserRetrieveModel | None:
        user = await self.users_repo.get_user_by_username_and_password(
            username=username, password=password, session=session
        )
        if user is None:
            return None
        session_uuid = uuid.uuid4()
        await self.users_repo.update_session_uuid(
            _id=user.id, session_uuid=session_uuid, session=session
        )
        user.session_uuid = session_uuid
        return user

    async def get_user_by_session_uuid(self, session_uuid: UUID, session: AsyncSession):
        user = await self.users_repo.get_user_by_session_uuid(
            session_uuid=session_uuid, session=session
        )
        return user

    async def get_post(self, session, _id):
        post = await self.post_repo.retrieve_with_comments(id=_id, session=session)
        comments = await self.comment_repo.get_comments_by_post_id(
            post_id=_id, session=session
        )
        post.comments = comments
        return post

    async def create_comment(self, comment_text, post_id, author_id, session):
        await self.comment_repo.create(comment=CommentCreateModel(
            text=comment_text,
            post_id=post_id,
            author_id=author_id,
        ), session=session)

    async def create_post(self, session, _id, name, description, image: UploadFile):
        with open(os.path.join("photos", image.filename), "wb") as buffer:
            buffer.write(image.file.read())
        post = await self.post_repo.create_post(session=session, post=PostCreateModel(
            name=name,
            description=description,
            photo=image.filename,
            author_id=_id,
        ))
        return post
