from uuid import UUID

from beanie import Document

from owow_backend.db.models import FileDocument


class FileDAO:
	@staticmethod
	async def create_file(file_name: str, file_summary: str) -> FileDocument:
		file_doc = FileDocument(file_name=file_name, file_summary=file_summary)
		return await file_doc.insert()  # noqa: ignore

	@staticmethod
	async def get_all_files() -> list[FileDocument]:
		return await FileDocument.find_all().to_list()

	@staticmethod
	async def get_file_by_id(file_id: UUID) -> FileDocument | Document | None:
		return await FileDocument.get(file_id)

	@staticmethod
	async def file_exists(file_name: str) -> bool:
		existing_file = await FileDocument.find_one(FileDocument.file_name == file_name)  # noqa: ignore
		return existing_file is not None
