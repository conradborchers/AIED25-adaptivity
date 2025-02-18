from abc import ABC
from loguru import logger
import traceback

DELIMITER = "#"
DEFAULT_RECOMMENDATIONS = [
    "[Ask your child to self-explain:] Explain to me what you have just done.",
    "[Ask your child to self-explain:] Explain to me what you did here.",
    "[Guide your child through the problem:] What is your next step and why?",
]

class ValidationException(Exception):
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class AbstractLLMClient(ABC):
    def __init__(self, modelKey: str | None):
        pass

    def sendPrompt(self, systemPrompt: str, modelPrompt: str) -> list[str]:
        raise NotImplementedError("Child class to override abstract sendPrompt method.")

    @staticmethod
    def _splitRecommendations(response: str) -> list[str]:
        recommendations = response.strip().split(DELIMITER)
        recommendations = [rec.strip() for rec in recommendations]
        if len(recommendations) != 3:
            logger.error(f"LLM responded with following text, which fails recommendation validation: {response}")
            logger.error("Using default static recommendations instead ...")
            raise ValidationException()
        return recommendations

    @classmethod
    def _getDefaultRecommendations(cls, *args) -> list[str]:
        return DEFAULT_RECOMMENDATIONS

    def sendPromptWithNoValidation(self, sysPrompt, userPrompt):
        raise NotImplementedError("Child class to override abstract sendPromptForTest method.")
