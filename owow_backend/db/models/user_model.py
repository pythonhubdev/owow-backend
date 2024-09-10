from beanie import Indexed

from owow_backend.db.models.base_document import BaseDocument


class UserDocument(BaseDocument):
	username: str = Indexed(str, unique=True)
	hashed_password: str

	class Settings:
		name = "users"
