from strands import Agent
from strands.multiagent.a2a import A2AServer
from strands_tools import http_request

from tools import add, div, get_current_time, mul, reverse_text, sqrt, sub

agent = Agent(
    name="Simple Utility Agent",
    description="A simple utility agent that posesses multiple tools for basic operations using the provided tools",
    tools=[add, sub, mul, div, reverse_text, get_current_time, http_request],
    callback_handler=None,
)

server = A2AServer(
    agent=agent,
    host="0.0.0.0",
    port=9000,
)

server.serve()
