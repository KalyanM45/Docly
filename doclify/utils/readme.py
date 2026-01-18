import time
from pathlib import Path
from rich.console import Console
from doclify.utils.llm import generate_doc
from doclify.utils.logger import get_logger

# Initialize logger and console
logger = get_logger(__name__)
console = Console()

def generate_readme_file(cache, config):
    """
    Generates the final README with clean uv-style output.
    """
    files = config.get("structure", [])
    if not files:
        logger.warning("README generation aborted: No files in structure.")
        console.print("[bold yellow]⚠ Warning:[/bold yellow] No files found in configuration structure.")
        return False

    logger.info("Starting README aggregation and generation.")
    
    with console.status("[bold cyan]Generating[/bold cyan] README.md", spinner="dots"):
        file_summaries = []
        for file_path, summary in cache.get("files", {}).items():
            if file_path in files: 
                 file_summaries.append(f"## File: {file_path}\n\n{summary}")
        
        if file_summaries:
            aggregated_summaries = "\n\n".join(file_summaries)
            final_readme = generate_doc(aggregated_summaries, type="final_summary")
            if final_readme:
                # Stripping ```markdown and ```
                final_readme = final_readme.replace('```markdown', '').replace('```', '')
        else:
            logger.warning("No summaries found in cache for README.")
            final_readme = "# Project Documentation\n\nNo summaries available."

        # Creating a directory for created READMEs
        version_dir = Path(".doclify/generated_artifacts/")
        version_dir.mkdir(exist_ok=True)
        artifact_path = version_dir / f"README-{time.strftime('%Y%m%d%H%M%S')}.md"
        artifact_path.write_text(final_readme, encoding="utf-8")
        logger.debug(f"Versioned artifact saved to {artifact_path}")

        readme_path = Path("README.md")
        if readme_path.exists():
            backup_path = Path(f"README-prev-{time.strftime('%Y%m%d%H%M%S')}.md")
            readme_path.rename(backup_path)
            logger.info(f"Existing README backed up to {backup_path}")

        readme_path.write_text(final_readme, encoding="utf-8")
        logger.info("README.md successfully updated.")

    return True
