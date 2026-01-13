from strands import tool
import requests
import json
import math
from datetime import datetime


# ---------------------------
# 🔢 MATH UTILITIES
# ---------------------------


@tool
def add(a: float, b: float):
    """Return the sum of two numbers."""
    return a + b


@tool
def sub(a: float, b: float):
    """Return the subtraction (a - b)."""
    return a - b


@tool
def mul(a: float, b: float):
    """Return multiplication of two numbers."""
    return a * b


@tool
def div(a: float, b: float):
    """Return division (a / b) with zero-check."""
    if b == 0:
        return "Error: Division by zero"
    return a / b


@tool
def sqrt(value: float):
    """Return square root of a number."""
    if value < 0:
        return "Error: Negative numbers not allowed"
    return math.sqrt(value)


# ---------------------------
# 📝 TEXT UTILITIES
# ---------------------------


@tool
def word_count(text: str):
    """Count the number of words in a text."""
    return len(text.split())


@tool
def reverse_text(text: str):
    """Reverse the given text."""
    return text[::-1]


@tool
def extract_json(text: str):
    """Try parsing the text into JSON."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return "Invalid JSON string"


# ---------------------------
# 🌐 BASIC HTTP TOOL
# ---------------------------


@tool
def fetch_url(url: str):
    """Fetch content from any URL (simple GET)."""
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "headers": dict(response.headers),
            "body": response.text[:500] + "...",  # limit
        }
    except Exception as e:
        return f"HTTP Error: {str(e)}"


# ---------------------------
# 🗂 FILE OPERATIONS (SAFE)
# ---------------------------


@tool
def write_file(filename: str, content: str):
    """Write text to a file."""
    with open(filename, "w") as f:
        f.write(content)
    return f"File '{filename}' written successfully"


@tool
def read_file(filename: str):
    """Read a file and return its content."""
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: File not found"


# ---------------------------
# 🕒 DATE / TIME TOOL
# ---------------------------


@tool
def get_current_time():
    """Return the current server timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------
# 🎲 RANDOM / MOCK DATA TOOL
# ---------------------------

import random


@tool
def random_number(min_value: int, max_value: int):
    """Return a random number between a and b."""
    return random.randint(min_value, max_value)


@tool
def random_choice(options: list):
    """Pick a random element from a list."""
    if not options:
        return "Error: Empty list"
    return random.choice(options)
