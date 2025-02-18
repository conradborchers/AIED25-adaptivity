from llm_recommendation_proxy.llm_client.aws_bedrock_llm_client import AWSBedrockLLMClient
from llm_recommendation_proxy.llm_client.openai_llm_client import OpenAILLMClient
from llm_recommendation_proxy.llm_client.abstract_llm_client import AbstractLLMClient
from llm_recommendation_proxy.prompt_formatter import PromptFormatter
from llm_recommendation_proxy.tutor_settings.few_shot_example_statements import FEW_SHOT_EXAMPLE_STATEMENTS
from llm_recommendation_proxy.tutor_settings.knowledge_components import KNOWLEDGE_COMPONENTS
from llm_recommendation_proxy.tutor_settings.persona_statements import PERSONA_STATEMENTS
from llm_recommendation_proxy.tutor_settings.tutor_id import TutorID
from llm_recommendation_proxy.util import formatStringList


class HTTPException(Exception):
    def __init__(self, errorCode: int, errorMessage: str):
        super().__init__(errorMessage)
        self.errorMessage = errorMessage
        if str(errorCode).startswith("4"):
            self.errorCode = f"{errorCode} Client-Side Request Error"
        elif str(errorCode).startswith("5"):
            self.errorCode = f"{errorCode} Internal Server Error"
        else:
            raise ValueError("HTTP error code must be 4XX or 5XX.")


_ROUTING_MAP = {
    "Llama3-8B": AWSBedrockLLMClient(modelKey="meta.llama3-8b-instruct-v1:0"),
    "Llama3-70B": AWSBedrockLLMClient(modelKey="meta.llama3-70b-instruct-v1:0"),
    "GPT-4o": OpenAILLMClient(modelKey="gpt-4o")
}


class Router(object):

    @staticmethod
    def processRequest(reqData: dict, mode: str = "inference") -> tuple[list[str], str]:

        if "model_id" not in reqData:
            raise HTTPException(400, "Request missing model ID")
        modelID = reqData["model_id"]

        if modelID not in _ROUTING_MAP:
            raise HTTPException(404, f"Model with ID: {modelID} is not supported. Available models: {_ROUTING_MAP.keys()}")
        client: AbstractLLMClient = _ROUTING_MAP[modelID]

        if "tutor_id" not in reqData:
            raise HTTPException(400, "Request missing tutor ID")
        tutorID = reqData["tutor_id"]

        if tutorID not in TutorID.getMembers():
            raise HTTPException(400, f"Tutor ID ({tutorID}) not supported. Available tutors: {TutorID.getMembers()}")
        personaStatement = PERSONA_STATEMENTS[tutorID]
        fewShotExampleStatement = FEW_SHOT_EXAMPLE_STATEMENTS[tutorID]

        if "KC" not in reqData:
            raise HTTPException(400, "Request missing knowledge component")
        KCs = formatStringList(reqData["KC"])

        for KC in KCs:
            if KC not in KNOWLEDGE_COMPONENTS:
                raise HTTPException(400, f"KC ({KC}) does not exist")
        KCDefs = [KNOWLEDGE_COMPONENTS[KC] for KC in KCs]

        if {"chat_history", "next_steps", "hints", "correct_step_history", "incorrect_step_history", "curr_question"} - set(reqData.keys()):
            raise HTTPException(400, f"Request data missing fields: { {'chat_history', 'next_step', 'used_hint', 'accuracy', 'curr_question'} - set(reqData.keys()) }")

        try:
            sysPrompt, userPrompt = PromptFormatter.format(
                personaStatement,
                fewShotExampleStatement,
                reqData["curr_question"],
                reqData["chat_history"],
                reqData["correct_step_history"],
                reqData["incorrect_step_history"],
                reqData["hints"],
                reqData["next_steps"],
                KCs,
                KCDefs
            )
            if mode == "inference":
                recommendations = client.sendPrompt(sysPrompt, userPrompt)
            elif mode == "test":
                recommendations = client.sendPromptWithNoValidation(sysPrompt, userPrompt)
            else:
                raise ValueError(f"Invalid mode '{mode}'")
        except Exception as e:
            raise HTTPException(500, repr(e))

        return recommendations, sysPrompt + userPrompt
