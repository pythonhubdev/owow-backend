"""1 models."""

from typing import Sequence, Type

from beanie import Document

from owow_backend.db.models.file_model import FileDocument
from owow_backend.db.models.user_model import UserDocument


def load_all_models() -> Sequence[Type[Document]]:
    """Load all models from this folder."""
    return [
        FileDocument,
        UserDocument,
    ]
