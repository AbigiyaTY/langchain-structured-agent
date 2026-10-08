from langchain_core.tools import tool


@tool
def search_tool(query: str) -> str:
    """Search for information about a topic."""
    return f"Search results for: {query}"


@tool
def wiki_tool(query: str) -> str:
    """Look up information from Wikipedia."""
    return f"Wikipedia information for: {query}"


@tool
def save_tool(content: str) -> str:
    """Save research content to a file."""
    with open("research.txt", "w", encoding="utf-8") as file:
        file.write(content)

    return "Research saved successfully."