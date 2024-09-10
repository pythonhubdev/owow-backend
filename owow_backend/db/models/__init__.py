"""1 models."""

from collections.abc import Sequence
from typing import Type

from beanie import Document

from owow_backend.db.models.file_model import FileDocument
from owow_backend.db.models.user_model import UserDocument


def load_all_models() -> Sequence[type[Document]]:
	"""Load all models from this folder."""
	return [
		FileDocument,
		UserDocument,
	]
