from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from owow_backend.core import DEFAULT_ROUTE_OPTIONS, APIResponse, ResponseUtils, StatusEnum
from owow_backend.web.api.user.controller import UserController
from owow_backend.web.api.user.schema import UserRequestSchema

user_router = APIRouter(prefix="/v1/users", tags=["Users"])


@user_router.post("", **DEFAULT_ROUTE_OPTIONS)
async def create_user(body: UserRequestSchema) -> APIResponse:
    try:
        result = await UserController.create_user(body.username, body.password)
        return APIResponse(
            status=StatusEnum.SUCCESS,
            message="User created successfully",
            data=jsonable_encoder(
                result.model_dump(
                    by_alias=True,
                ),
            ),
            status_code=201,
        )
    except Exception as e:
        return ResponseUtils.create_error_response(status_code=500, message=str(e))
