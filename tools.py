from datetime import datetime
from langchain_core.tools import tool

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

@tool
def search_tool(query: str) -> str:
    """Search for information about a topic."""
    return f"Search results for: {query}"


@tool
def wiki_tool(query: str) -> str:
    """Look up information from Wikipedia."""
    return f"Wikipedia information for: {query}"

@tool
def save_tool(data: str, filename: str = "research_output.txt") -> str:
    """Save research data to a text file with a timestamp."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    formatted_text = (
        f"--- Research Output ---\n"
        f"Timestamp: {timestamp}\n\n"
        f"{data}\n\n"
    )

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"