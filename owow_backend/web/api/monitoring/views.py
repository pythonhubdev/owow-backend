from fastapi import APIRouter

from owow_backend.core import DEFAULT_ROUTE_OPTIONS, APIResponse, StatusEnum

health_router = APIRouter(tags=["Monitoring", "Health"])


@health_router.get("/health", **DEFAULT_ROUTE_OPTIONS)
def health_check() -> APIResponse:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
    return APIResponse(
        status=StatusEnum.SUCCESS,
        message="The project is healthy.",
    )
