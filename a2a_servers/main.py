from strands import Agent
from strands.multiagent.a2a import A2AServer

from tools import add, div, get_current_time, mul, reverse_text, sqrt, sub

agent = Agent(
    name="Simple Utility Agent",
    description="A simple utility agent that posesses multiple tools for basic math oprations, string oprations and to retrieve current time using the provided tools",
    tools=[add, sub, mul, div, reverse_text, get_current_time],
    callback_handler=None,
)

server = A2AServer(agent=agent)

server.serve()
