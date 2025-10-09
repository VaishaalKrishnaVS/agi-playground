from typing import Any
from strands import Agent
from strands.types.agent import AgentInput
from strands.tools.executors import ConcurrentToolExecutor
from strands_tools import http_request
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="agents_workflow.log",
    filemode="a",
)
log = logging.getLogger(__name__)


class LoggingConcurrentToolExecutor(ConcurrentToolExecutor):
    """Concurrent tool executor with detailed logging."""

    async def _execute(
        self, agent, tool_uses, tool_results, cycle_trace, cycle_span, invocation_state
    ):
        if tool_uses:
            log.info(f"🔧 Executing {len(tool_uses)} tools in parallel:")
            for i, tool_use in enumerate(tool_uses):
                # Handle both dict and object formats
                if hasattr(tool_use, "name"):
                    name = tool_use.name
                    input_data = getattr(tool_use, "input", "N/A")
                elif isinstance(tool_use, dict):
                    name = tool_use.get("name", "unknown")
                    input_data = tool_use.get("input", "N/A")
                else:
                    name = str(tool_use)
                    input_data = "N/A"
                log.info(f"   Tool {i+1}: {name} - {input_data}")

        start_time = time.time()
        async for event in super()._execute(
            agent, tool_uses, tool_results, cycle_trace, cycle_span, invocation_state
        ):
            yield event

        if tool_uses:
            execution_time = time.time() - start_time
            log.info(
                f"🔧 All {len(tool_uses)} tools completed in {execution_time:.1f}s"
            )
            for i, result in enumerate(tool_results):
                if hasattr(result, "content") and result.content:
                    content_preview = (
                        str(result.content)[:100] + "..."
                        if len(str(result.content)) > 100
                        else str(result.content)
                    )
                    log.info(f"   Result {i+1}: {content_preview}")
                elif isinstance(result, dict) and result.get("content"):
                    content = str(result["content"])
                    content_preview = (
                        content[:100] + "..." if len(content) > 100 else content
                    )
                    log.info(f"   Result {i+1}: {content_preview}")


from prompts import (
    ANALYST_AGENT_PROMPT,
    RESEARCH_AGENT_PROMPT,
    WRITER_AGENT_PROMPT,
)


class LoggingAgent(Agent):
    def __init__(self, agent_name: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent_name = agent_name or self.__class__.__name__
        log.info(f"🤖 AGENT INITIALIZED: {self.agent_name}")
        log.info(
            f"   System Prompt: {self.system_prompt[:100]}..."
            if len(self.system_prompt) > 100
            else f"   System Prompt: {self.system_prompt}"
        )

    def __call__(self, prompt: AgentInput = None, **kwargs: Any):
        start_time = time.time()
        log.info(f"🚀 {self.agent_name} Starting")

        try:
            result = super().__call__(prompt, **kwargs)
            execution_time = time.time() - start_time
            log.info(f"✅ {self.agent_name} Complete ({execution_time:.1f}s)")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            log.error(f"❌ {self.agent_name} Failed ({execution_time:.1f}s): {str(e)}")
            raise


researcher_agent = LoggingAgent(
    agent_name="RESEARCHER_AGENT",
    system_prompt=RESEARCH_AGENT_PROMPT,
    tools=[http_request],
    tool_executor=LoggingConcurrentToolExecutor(),
)
analyst_agent = LoggingAgent(
    agent_name="ANALYST_AGENT", system_prompt=ANALYST_AGENT_PROMPT
)
writer_agent = LoggingAgent(
    agent_name="WRITER_AGENT", system_prompt=WRITER_AGENT_PROMPT
)
