from lorax.types import Response
from predibase import Predibase

from owow_backend.settings import settings


class PredibaseService:
	def __init__(self) -> None:
		self.predibase_client = Predibase(api_token=settings.predibase_token)
		self.lorax_client = self.predibase_client.deployments.async_client("llama-3-1-8b-instruct")

	async def generate_summary(self, text: str) -> Response:
		result: Response = await self.lorax_client.generate(
			f"""[INST] Summarize the following text in exactly 3 short, concise sentences. Focus on the most crucial
            points. Do not include any introductory phrases like "Here is a summary" or "This text discusses".
            Start directly with the summary: \n" + {text} + "\n" + "[/INST]""",
			max_new_tokens=128,
		)
		return result
