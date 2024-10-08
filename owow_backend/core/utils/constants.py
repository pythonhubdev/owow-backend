from typing import TypedDict

from fastapi.security import HTTPBasic
from pydantic import BaseModel

from owow_backend.core.schema.common_response_schema import CommonResponseSchema


class RouteOptions(TypedDict):
	response_model_exclude_none: bool
	response_model: type[BaseModel]


DEFAULT_ROUTE_OPTIONS: RouteOptions = {
	"response_model_exclude_none": True,
	"response_model": CommonResponseSchema,
}

security = HTTPBasic()
