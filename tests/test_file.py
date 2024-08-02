import base64
from pathlib import Path
from typing import Any, AsyncGenerator, Generator
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from lorax.types import Response

from owow_backend.db.models import FileDocument, UserDocument
from owow_backend.service import PredibaseService
from owow_backend.web.api.user.controller import UserController

valid_credentials = base64.b64encode(b"testuser:testpassword").decode("utf-8")


@pytest.fixture(autouse=True)
async def user() -> AsyncGenerator[UserDocument, None]:
    user = await UserController.create_user("testuser", "testpassword")
    yield user


@pytest.fixture(autouse=True)
async def setup_file() -> AsyncGenerator[FileDocument, None]:
    file = FileDocument(
        file_name="test.docx",
        file_summary="This is a test summary",
    )
    file = await file.insert()  # type: ignore
    yield file


@pytest.fixture
def mock_predibase_service() -> Generator[AsyncMock, Any, Any]:
    with patch.object(PredibaseService, "generate_summary", new_callable=AsyncMock) as mock:
        mock.return_value = Response(
            generated_text="This is a test summary",
        )
        yield mock


async def test_upload_file(client: AsyncClient, clean_db: None, mock_predibase_service: None) -> None:
    file_path = Path("storage/Sample.docx")

    assert file_path.exists(), f"Test file not found: {file_path}"
    with open(file_path, "rb") as file:
        response = await client.post(
            "/v1/files",
            files={
                "file": (
                    file_path.name,
                    file,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ),
            },
            headers={"Authorization": f"Basic {valid_credentials}"},
        )
    assert response.status_code == 201
    data = response.json()
    assert "_id" in data["data"]


async def test_upload_file_pdf(client: AsyncClient, clean_db: None, mock_predibase_service: None) -> None:
    file_path = Path("storage/Interview Post.pdf")

    assert file_path.exists(), f"Test file not found: {file_path}"
    with open(file_path, "rb") as file:
        response = await client.post(
            "/v1/files",
            files={
                "file": (
                    file_path.name,
                    file,
                    "application/pdf",
                ),
            },
            headers={"Authorization": f"Basic {valid_credentials}"},
        )
    assert response.status_code == 201
    data = response.json()
    assert "_id" in data["data"]


async def test_upload_file_pptx(client: AsyncClient, clean_db: None, mock_predibase_service: None) -> None:
    file_path = Path("storage/sample.pptx")

    assert file_path.exists(), f"Test file not found: {file_path}"
    with open(file_path, "rb") as file:
        response = await client.post(
            "/v1/files",
            files={
                "file": (
                    file_path.name,
                    file,
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                ),
            },
            headers={"Authorization": f"Basic {valid_credentials}"},
        )
    assert response.status_code == 201
    data = response.json()
    assert "_id" in data["data"]


async def test_get_file_list(client: AsyncClient, clean_db: None) -> None:
    response = await client.get(
        "/v1/files",
        headers={"Authorization": f"Basic {valid_credentials}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1


async def test_get_file_summary(client: AsyncClient, clean_db: None, setup_file: FileDocument) -> None:
    response = await client.get(
        f"/v1/files/{setup_file.id}",
        headers={"Authorization": f"Basic {valid_credentials}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "fileSummary" in data["data"]
