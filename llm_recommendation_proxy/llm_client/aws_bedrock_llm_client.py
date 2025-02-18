from functools import cache
from loguru import logger
from botocore.exceptions import ClientError
from tenacity import retry, stop_after_attempt, wait_none, retry_if_exception_type
from llm_recommendation_proxy.llm_client.abstract_llm_client import AbstractLLMClient, ValidationException
import boto3
from llm_recommendation_proxy.llm_client.inference_settings import InferenceSettings
import json

LLAMA3_PROMPT_FORMAT = \
"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system-prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user-prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""


class AWSBedrockLLMClient(AbstractLLMClient):
    def __init__(self, modelKey: str = "meta.llama3-8b-instruct-v1:0"):
        super().__init__(modelKey)
        self.modelKey = modelKey

        session = boto3.Session()
        credentials = session.get_credentials()
        accessKey = credentials.access_key
        secretKey = credentials.secret_key

        self.bedrockClient = boto3.client(
            'bedrock-runtime',
            region_name='us-east-1',
            aws_access_key_id=accessKey,
            aws_secret_access_key=secretKey
        )

    @cache
    @retry(stop=stop_after_attempt(2),
           wait=wait_none(),
           retry_error_callback=AbstractLLMClient._getDefaultRecommendations,
           retry=retry_if_exception_type(ValidationException))
    def sendPrompt(self, systemPrompt: str, userPrompt: str) -> list[str]:
        if "llama3" in self.modelKey:
            prompt = LLAMA3_PROMPT_FORMAT.replace("{system-prompt}", systemPrompt).replace("{user-prompt}", userPrompt)
        else:
            prompt = systemPrompt + "\n" + userPrompt
        nativeRequest = {
            "prompt": prompt,
            "max_gen_len": InferenceSettings.MAX_TOKENS,
            "temperature": InferenceSettings.TEMPERATURE,
        }
        request = json.dumps(nativeRequest)
        try:
            response = self.bedrockClient.invoke_model(modelId=self.modelKey, body=request)
        except (ClientError, Exception) as e:
            logger.error(f"ERROR: Can't invoke '{self.modelKey}'. Reason: {e}")
            raise e

        model_response = json.loads(response["body"].read())
        response_text = model_response["generation"]
        recommendations = self._splitRecommendations(response_text)
        return recommendations

    @cache
    def sendPromptWithNoValidation(self, systemPrompt: str, userPrompt: str) -> str:
        if "llama3" in self.modelKey:
            prompt = LLAMA3_PROMPT_FORMAT.replace("{system-prompt}", systemPrompt).replace("{user-prompt}", userPrompt)
        else:
            prompt = systemPrompt + "\n" + userPrompt
        nativeRequest = {
            "prompt": prompt,
            "max_gen_len": InferenceSettings.MAX_TOKENS,
            "temperature": InferenceSettings.TEMPERATURE,
        }
        request = json.dumps(nativeRequest)
        try:
            response = self.bedrockClient.invoke_model(modelId=self.modelKey, body=request)
        except (ClientError, Exception) as e:
            logger.error(f"ERROR: Can't invoke '{self.modelKey}'. Reason: {e}")
            raise e

        model_response = json.loads(response["body"].read())
        return model_response["generation"]


if __name__ == "__main__":
    client = AWSBedrockLLMClient()
    print(client.sendPrompt("You are a useful assistant", "How are you?"))
