import enum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, enum.Enum):
	"""Possible log levels."""

	NOTSET = "NOTSET"
	DEBUG = "DEBUG"
	INFO = "INFO"
	WARNING = "WARNING"
	ERROR = "ERROR"
	FATAL = "FATAL"


class Settings(BaseSettings):
	"""
	Application settings.

	These parameters can be configured
	with environment variables.
	"""

	host: str = "0.0.0.0"
	port: int = 8000
	workers_count: int = 1
	reload: bool = False
	environment: str = "DEV"
	log_level: LogLevel = LogLevel.INFO
	opentelemetry_endpoint: str | None = None
	mongo_host: str = "mongodb://localhost:27017"
	predibase_token: str | None = None

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
	)


@lru_cache
def _settings() -> Settings:
	return Settings()  # type: ignore


settings: Settings = _settings()
