from fastapi import APIRouter

from owow_backend.core import DEFAULT_ROUTE_OPTIONS, APIResponse, StatusEnum
from owow_backend.web.api.echo.schema import Message

echo_router = APIRouter(prefix="/echo", tags=["Echo"])


@echo_router.post("", **DEFAULT_ROUTE_OPTIONS)
async def send_echo_message(
	incoming_message: Message,
) -> APIResponse:
	"""
	Sends echo back to user.

	:param incoming_message: incoming message.
	:returns: message same as the incoming.
	"""
	return APIResponse(
		status=StatusEnum.SUCCESS,
		message=incoming_message.message,
	)
