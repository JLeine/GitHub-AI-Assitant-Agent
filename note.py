from langchain_core.tools import tool

@tool
def note_tool(note):
    """
    saves a note to a local file

    Args:
        note: the text note to save
    """
    try:
        with open("data/notes.txt", "a") as f:
            f.write(note + "\n")
    except Exception as e:
        print(f"Error saving note: {e}")
