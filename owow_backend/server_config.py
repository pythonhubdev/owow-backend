from hypercorn import Config

from owow_backend.settings import settings


class HypercornConfig(Config):
	bind = [f"{settings.host}:{settings.port}"]
	workers = settings.workers_count
	use_reloader = settings.reload
	accesslog = None
	errorlog = None
