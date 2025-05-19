"""
An Agno-based agent mirroring the original LangChain-Anthropic workflow 
from src/llm/llm_chain_of_thought.py:
"""
import os
import inspect

# Ensure project root is on PYTHONPATH for local modules
import path_helper
path_helper.add_project_path()

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools import tool

# Import your domain-specific modules
from office_plans.office_plan import define_office_plan
from office_description.create_prompt import create_prompt
from llm.llm_feedback import give_llm_feedback as _give_llm_feedback
from llm.llm_visualization import visualize_llm_solution
from typing import List, Tuple, TypedDict


WallConfig = Tuple[float, float, float]

tool_sig = inspect.signature(_give_llm_feedback)
# Dynamically wrap the existing feedback function as a generic Agno tool
@tool(
    name="feedback_tool",
    description="Provide feedback to the LLM given with text and scores",
    sanitize_arguments=True,
    strict=False,
)
def feedback_tool(iteration: int, moveable_walls: List[WallConfig]) -> str:
    """
    Wrapper that filters kwargs to match give_llm_feedback signature and invokes it.
    """
    feedback = _give_llm_feedback(iteration=iteration, moveable_walls=moveable_walls)
    print(feedback)
    return feedback

# Load your API key from environment
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("Please set the ANTHROPIC_API_KEY environment variable")

agent = Agent(
    model=Claude(
        id="claude-3-7-sonnet-20250219",
        temperature=0,
        max_tokens=1024,
        api_key=api_key,
    ),
    tools=[feedback_tool],
    instructions=["You are a helpful assistant."],
    show_tool_calls=True,
    markdown=False,
)


def main():
    # Prepare the initial query
    coords, windows, doors, desks, persons, dist_persons, objects, dist_points, _ = define_office_plan()
    prompt = create_prompt(coords, windows, doors, desks, persons, dist_persons, objects, dist_points)
    
    # Run the agent: stream reasoning, intermediate steps, and tool calls
    agent.print_response(
        prompt,
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True,
        markdown=True,
    )


if __name__ == "__main__":
    # Example PowerShell installation:
    # > pip install agno anthropic
    main()
