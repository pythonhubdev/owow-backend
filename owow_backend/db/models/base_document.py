from datetime import datetime

from beanie import Document
from pydantic import ConfigDict, Field

from owow_backend.core import CaseConverter


class BaseDocument(Document):
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime | None = None

	model_config = ConfigDict(
		alias_generator=CaseConverter.camelize,
		populate_by_name=True,
	)
