from owow_backend.db.models import UserDocument


class UserDAO:
	@staticmethod
	async def create_user(username: str, hashed_password: str | bytes) -> UserDocument:
		user = UserDocument(username=username, hashed_password=hashed_password)
		return await user.insert()  # noqa: ignore

	@staticmethod
	async def get_user(username: str) -> UserDocument | None:
		return await UserDocument.find_one(UserDocument.username == username)  # noqa: ignore

	@staticmethod
	async def user_exists(username: str) -> bool:
		user = await UserDAO.get_user(username)
		return user is not None
