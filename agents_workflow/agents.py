from typing import Any
from strands import Agent
from strands.types.agent import AgentInput
from strands_tools import http_request
import logging
import time
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="agents_workflow.log",
    filemode="a",
)
log = logging.getLogger(__name__)


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
        log.info(
            f"   Tools Available: {[tool.__name__ if hasattr(tool, '__name__') else str(tool) for tool in (self.tools or [])]}"
        )

    def __call__(self, prompt: AgentInput = None, **kwargs: Any):
        start_time = time.time()
        log.info(f"\n{'='*80}")
        log.info(f"🚀 AGENT EXECUTION START: {self.agent_name}")
        log.info(f"📝 INPUT PROMPT: {prompt}")
        log.info(f"⚙️  KWARGS: {json.dumps(kwargs, indent=2, default=str)}")

        try:
            result = super().__call__(prompt, **kwargs)
            execution_time = time.time() - start_time

            log.info(f"✅ AGENT EXECUTION COMPLETE: {self.agent_name}")
            log.info(f"⏱️  Execution Time: {execution_time:.2f} seconds")
            log.info(
                f"📤 FINAL RESULT: {str(result)[:500]}..."
                if len(str(result)) > 500
                else f"📤 FINAL RESULT: {result}"
            )
            log.info(f"{'='*80}\n")

            return result
        except Exception as e:
            execution_time = time.time() - start_time
            log.error(f"❌ AGENT EXECUTION FAILED: {self.agent_name}")
            log.error(f"⏱️  Execution Time: {execution_time:.2f} seconds")
            log.error(f"🚨 ERROR: {str(e)}")
            log.error(f"{'='*80}\n")
            raise

    async def stream_async(self, prompt: AgentInput = None, **kwargs: Any):
        start_time = time.time()
        log.info(f"\n{'='*80}")
        log.info(f"🚀 AGENT STREAMING START: {self.agent_name}")
        log.info(f"📝 INPUT PROMPT: {prompt}")
        log.info(f"⚙️  KWARGS: {json.dumps(kwargs, indent=2, default=str)}")

        chunk_count = 0
        full_response = ""

        try:
            async for chunk in super().stream_async(prompt, **kwargs):
                chunk_count += 1
                chunk_str = str(chunk)
                full_response += chunk_str
                log.info(f"📦 CHUNK {chunk_count}: {chunk_str}")
                yield chunk

            execution_time = time.time() - start_time
            log.info(f"✅ AGENT STREAMING COMPLETE: {self.agent_name}")
            log.info(f"⏱️  Execution Time: {execution_time:.2f} seconds")
            log.info(f"📊 Total Chunks: {chunk_count}")
            log.info(
                f"📤 FULL RESPONSE: {full_response[:500]}..."
                if len(full_response) > 500
                else f"📤 FULL RESPONSE: {full_response}"
            )
            log.info(f"{'='*80}\n")

        except Exception as e:
            execution_time = time.time() - start_time
            log.error(f"❌ AGENT STREAMING FAILED: {self.agent_name}")
            log.error(f"⏱️  Execution Time: {execution_time:.2f} seconds")
            log.error(f"📊 Chunks Processed: {chunk_count}")
            log.error(f"🚨 ERROR: {str(e)}")
            log.error(f"{'='*80}\n")
            raise


researcher_agent = LoggingAgent(
    agent_name="RESEARCHER_AGENT",
    system_prompt=RESEARCH_AGENT_PROMPT,
    tools=[http_request],
)
analyst_agent = LoggingAgent(
    agent_name="ANALYST_AGENT", system_prompt=ANALYST_AGENT_PROMPT
)
writer_agent = LoggingAgent(
    agent_name="WRITER_AGENT", system_prompt=WRITER_AGENT_PROMPT
)
