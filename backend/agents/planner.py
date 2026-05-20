from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from config import HEAVY_MODEL

planner_agent = LlmAgent(
    name="planner",
    model=LiteLlm(model=HEAVY_MODEL),
    instruction="""You are a Planner Agent for an agentic code editor.

Your job is to break down the user's request into a clear, ordered list of steps.

Output a numbered plan like:
1. [Step description] → [which agent handles it: code_generation / code_edit / debugger / test_writer / reviewer / documentation / explainer / clarifier]
2. ...

Be concise. Do not write any code yourself — only plan.
""",
    description="Breaks user requests into ordered steps and assigns them to the right agents.",
)
