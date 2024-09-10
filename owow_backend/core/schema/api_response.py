from typing import Any

from starlette.responses import JSONResponse

from owow_backend.core.schema.common_response_schema import CommonResponseSchema
from owow_backend.core.utils.enums import StatusEnum


class APIResponse(JSONResponse):
	def __init__(
		self,
		status: StatusEnum,
		message: str,
		data: Any = None,
		status_code: int = 200,
		headers: dict[Any, Any] | None = None,
	):
		content = CommonResponseSchema(status=status, message=message, data=data).model_dump(exclude_none=True)
		super().__init__(content=content, status_code=status_code, headers=headers)


class ResponseUtils:
	@staticmethod
	def create_error_response(status_code: int, message: str) -> APIResponse:
		return APIResponse(status=StatusEnum.ERROR, message=message, status_code=status_code)
