from typing import Any

from pydantic import BaseModel, ConfigDict

from owow_backend.core.utils.enums import StatusEnum


class CommonResponseSchema(BaseModel):
	status: StatusEnum
	message: str
	data: dict[Any, Any] | list[dict[Any, Any]] | None = None
	model_config = ConfigDict(
		json_schema_extra={
			"example": {
				"status": "success",
				"message": "The project is healthy.",
			},
		},
	)
