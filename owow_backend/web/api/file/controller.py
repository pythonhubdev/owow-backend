import os
import uuid

from fastapi import HTTPException, UploadFile
from lorax.types import Response

from owow_backend.db.dao.file_dao import FileDAO
from owow_backend.db.models import FileDocument
from owow_backend.service import DocService, PredibaseService

ALLOWED_EXTENSIONS = {".docx", ".pptx", ".pdf"}
UPLOAD_FOLDER = "storage/"


class FileController:
	@staticmethod
	async def upload_file(file: UploadFile) -> FileDocument:
		os.makedirs(UPLOAD_FOLDER, exist_ok=True)
		_, extension = os.path.splitext(file.filename)  # type: ignore
		if extension.lower() not in ALLOWED_EXTENSIONS:  # type: ignore
			raise HTTPException(status_code=400, detail="File type not allowed")
		if await FileDAO.file_exists(file.filename):  # type: ignore
			raise HTTPException(status_code=400, detail="File already exists")

		file_path: str = os.path.join(UPLOAD_FOLDER + file.filename)  # type: ignore
		with open(file_path, "wb") as buffer:
			buffer.write(await file.read())

		file_text: str = DocService().extract_text_from_file(file_path)
		predibase_response: Response = await PredibaseService().generate_summary(file_text)
		file_summary = predibase_response.generated_text
		if "The most crucial points of the agreement are: " in file_summary:
			file_summary = file_summary.replace("The most crucial points of the agreement are: ", "")
		return await FileDAO.create_file(file.filename, file_summary)  # type: ignore

	@staticmethod
	async def get_all_files() -> list[FileDocument]:
		return await FileDAO.get_all_files()

	@staticmethod
	async def get_file_by_id(file_id: uuid.UUID) -> FileDocument:
		file = await FileDAO.get_file_by_id(file_id)
		if not file:
			raise HTTPException(status_code=404, detail="File not found")
		return file
