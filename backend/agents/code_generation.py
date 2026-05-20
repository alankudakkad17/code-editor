from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from config import HEAVY_MODEL

code_generation_agent = LlmAgent(
    name="code_generation",
    model=LiteLlm(model=HEAVY_MODEL),
    instruction="""You are a Code Generation Agent for an agentic code editor.

Your job is to write new, high-quality code based on the user's request.

Guidelines:
- Write clean, idiomatic code in the language the user specifies (or infer from context)
- Do not add unnecessary comments or boilerplate
- Return ONLY the code block, clearly formatted with the correct language tag
- After the code, add a brief 2-3 line summary of what was written
""",
    description="Writes new code from natural language descriptions.",
)
