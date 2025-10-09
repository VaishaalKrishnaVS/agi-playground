from strands import Agent, agent, tool
from strands_tools import calculator, current_time


@tool
def letter_counter(word: str, letter: str) -> int:
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0
    if len(letter) != 1:
        raise ValueError("The letter parameter should be a single character")

    return word.lower().count(letter.lower())


agent = Agent(tools=[calculator, current_time, letter_counter])

message = """
I have 4 requests:
1. What is the time right now?
2. Calculate 2345432345/4323443
3. Tell me how many letter R's are in word "strawberry"
"""

agent(prompt=message)
