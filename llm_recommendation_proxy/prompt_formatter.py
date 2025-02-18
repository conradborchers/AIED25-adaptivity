from loguru import logger

from llm_recommendation_proxy.util import formatStringList

PROMPT_TEMPLATE = \
"""
Here are some examples of responses.

{few-shot-examples}

This is the equation your child is working on: {problem}. They need to solve for x.

{correct-steps-statement}

{hint-statement}

{incorrect-steps-statement}

Here are suggested next steps:
{next-steps}

This problem is examining the following knowledge components (KC). The following are KC's being tested in the problem using the <KC name>: <KC definition> format:
{knowledge-components-statement}

The elements in this list are messages that have been sent in a conversation between a middle school student and their parent about a math problem (in order).
Use these messages to generate 1 to 2 sentence responses that a parent would say to their child at this point in the conversation.
Include a short justifications in square brackets at the start of each message, such as [Ask to self explain] "Tell me what you mean",
[Praise your child for a correct attempt] "Great job on solving that math problem.", [Your child has made an error] "I appreciate your effort."
Do not include quotation marks. Do not give away the answer. Do not directly point out errors. Generate 3 different responses, separated by the # symbol, like this: message 1 # message 2 # message 3 #
Use the tone that the parent has been using in previous messages to generate messages with similar tone. This is the list, delimited with square brackets: [
{chat-history}
]
"""


class PromptFormatter(object):
    @classmethod
    def format(cls,
               personaStatement: str,
               fewShotExampleStatement: str,
               currentProblem: str,
               chatHistory: list[str],
               correctStepHistory: list[str] | str,
               incorrectStepHistory: list[str] | str,
               hints: list[str] | str,
               suggestedNextSteps: list[str],
               KC: list[str],
               KCDefinition: list[str]) -> tuple[str, str]:
        """
        Formats the prompt template and returns 1) system prompt and 2) user prompt
        """
        correctStepHistory = formatStringList(correctStepHistory)
        incorrectStepHistory = formatStringList(incorrectStepHistory)
        hints = formatStringList(hints)

        hintStatement = f"Your child did use a hint. Here are hints used delimited by ';': {'; '.join(hints)}." if hints \
                        else f"You child did not use a hint for this problem."
        correctStepsStatement = f"Your child has taken the following correct steps to solve the problem: {'; '.join(correctStepHistory)}." if correctStepHistory \
                                else f"Your child has not taken a step in solve the problem."
        incorrectStepsStatement = f"Your child has taken the following wrong attempt to solve the current step: {'; '.join(incorrectStepHistory)}." if incorrectStepHistory \
                                  else f"Your child has not made an error in solving the current step."
        KCStatement = "\n".join([f"{kc}: {kcDef}" for kc, kcDef in zip(KC, KCDefinition)])

        userPrompt = PROMPT_TEMPLATE.replace("{few-shot-examples}", fewShotExampleStatement) \
                                    .replace("{hint-statement}", hintStatement) \
                                    .replace("{correct-steps-statement}", correctStepsStatement) \
                                    .replace("{incorrect-steps-statement}", incorrectStepsStatement) \
                                    .replace("{next-steps}", "\n".join(suggestedNextSteps)) \
                                    .replace("{knowledge-components-statement}", KCStatement) \
                                    .replace("{problem}", currentProblem) \
                                    .replace("{chat-history}", "\n".join(chatHistory))

        logger.info(f"User prompt after formating is:\n{userPrompt}")

        return personaStatement, userPrompt
