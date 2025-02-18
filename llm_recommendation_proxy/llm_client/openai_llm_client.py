import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_none, retry_if_exception_type
from llm_recommendation_proxy.llm_client.abstract_llm_client import AbstractLLMClient, ValidationException
from functools import cache
from llm_recommendation_proxy.llm_client.inference_settings import InferenceSettings


class OpenAILLMClient(AbstractLLMClient):

    @staticmethod
    def _readAPIKey():
        # try OS env variables first
        key = os.environ.get('OPENAI_API_KEY')
        if key:
            return key
        key = os.environ.get('OPEN_AI_API_KEY')
        if key:
            return key
        # if variable does not exist, try to look for a key file
        with open("bedrock/openai.key", "r") as file:
            key = file.read()
        return key

    def __init__(self, modelKey: str = "gpt-4o"):
        super().__init__(modelKey)
        self.modelKey = modelKey
        self.openAIClient = OpenAI(api_key=self._readAPIKey())

    @cache
    @retry(stop=stop_after_attempt(2),
           wait=wait_none(),
           retry_error_callback=AbstractLLMClient._getDefaultRecommendations,
           retry=retry_if_exception_type(ValidationException))
    def sendPrompt(self, systemPrompt: str, userPrompt: str) -> list[str]:
        response = self.openAIClient.chat.completions.create(
            model=self.modelKey,
            messages=[
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": userPrompt},
            ],
            max_tokens=InferenceSettings.MAX_TOKENS,
            temperature=InferenceSettings.TEMPERATURE
        )
        text = response.choices[0].message.content
        recommendations = self._splitRecommendations(text)
        return recommendations

    @cache
    def sendPromptWithNoValidation(self, systemPrompt: str, userPrompt: str) ->str:
        response = self.openAIClient.chat.completions.create(
            model=self.modelKey,
            messages=[
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": userPrompt},
            ],
            max_tokens=InferenceSettings.MAX_TOKENS,
            temperature=InferenceSettings.TEMPERATURE
        )
        text = response.choices[0].message.content
        return text


if __name__ == "__main__":
    client = OpenAILLMClient()
    print(client.sendPrompt("You are a useful assistant", "How are you?"))
