import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials

from owow_backend.core import APIResponse, ResponseUtils, StatusEnum, security
from owow_backend.db.models import FileDocument
from owow_backend.web.api.file.controller import FileController
from owow_backend.web.api.user.controller import UserController

file_router = APIRouter(prefix="/v1/files", tags=["Files"])


async def get_current_username(
	credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
	return await UserController.authenticate_user(credentials)


@file_router.post("")
async def upload_file(
	username: Annotated[str, Depends(get_current_username)],
	file: UploadFile = File(...),
) -> APIResponse:
	file_service = FileController()
	try:
		result = await file_service.upload_file(file)
		return APIResponse(
			status=StatusEnum.SUCCESS,
			message="File uploaded successfully",
			data=jsonable_encoder(
				result.model_dump(
					by_alias=True,
				),
			),
			status_code=201,
		)
	except HTTPException as e:
		return ResponseUtils.create_error_response(e.status_code, e.detail)
	except Exception as e:
		return ResponseUtils.create_error_response(500, str(e))


@file_router.get("")
async def list_files(username: Annotated[str, Depends(get_current_username)]) -> APIResponse:
	file_service = FileController()
	try:
		result: list[FileDocument] = await file_service.get_all_files()
		if len(result) == 0:
			return ResponseUtils.create_error_response(404, "No files found")
		return APIResponse(
			status=StatusEnum.SUCCESS,
			message="Files fetched successfully",
			data=[
				jsonable_encoder(
					res.model_dump(
						exclude={"file_summary"},
						by_alias=True,
					),
				)
				for res in result
			],
		)
	except Exception as e:
		return ResponseUtils.create_error_response(500, str(e))


@file_router.get("/{file_id}")
async def get_file(file_id: uuid.UUID, username: Annotated[str, Depends(get_current_username)]) -> APIResponse:
	file_service = FileController()
	try:
		result: FileDocument = await file_service.get_file_by_id(file_id)
		return APIResponse(
			status=StatusEnum.SUCCESS,
			message="Summary fetched successfully",
			data=jsonable_encoder(
				result.model_dump(
					exclude={"file_name", "created_at"},
					exclude_none=True,
					by_alias=True,
				),
			),
		)
	except HTTPException as e:
		return ResponseUtils.create_error_response(e.status_code, e.detail)
	except Exception as e:
		return ResponseUtils.create_error_response(500, str(e))
