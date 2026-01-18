from pathlib import Path
from doclify.utils.logger import get_logger

# Initialize the logger
logger = get_logger(__name__)

def extract_file_content(file_path: str) -> str:
    """
    Reads and returns the content of the file.
    Example output format:
    File: <path>
    ```<extension>
    <content>
    ```
    """
    path = Path(file_path)
    if not path.exists():
        logger.warning(f"File not found: {file_path}")
        return f"File not found: {file_path}"
    
    try:
        content = path.read_text(encoding="utf-8")
        ext = path.suffix.lstrip(".") or "txt"
        
        # FIXED: Use file_path (with underscore)
        logger.info(f"Extraction successful for {file_path}")
        
        return f"File: {file_path}\n```{ext}\n{content}\n```"
        
    except Exception as e:
        # Log the actual error with traceback for debugging
        logger.error(f"Error reading file {file_path}: {e}", exc_info=True)
        return f"Error reading file {file_path}: {e}"