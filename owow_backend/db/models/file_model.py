from uuid import UUID, uuid4

from pydantic import Field

from owow_backend.db.models.base_document import BaseDocument


class FileDocument(BaseDocument):
	id: UUID = Field(default_factory=uuid4, alias="_id")  # type: ignore
	file_name: str
	file_summary: str

	class Settings:
		name = "files"
