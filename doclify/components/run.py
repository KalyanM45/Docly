import yaml
import click
import time
import os
import json
import re
from pathlib import Path
from rich.console import Console
from doclify.utils.extract import extract_file_content
from doclify.utils.llm import generate_doc
from doclify.utils.file_utils import load_cache, save_cache
from doclify.schema.schema import FileSummaries
from doclify.utils.readme import generate_readme_file
from doclify.utils.logger import get_logger

# Initialize production-level logger and clean console
logger = get_logger(__name__)
console = Console()

def run_docs():
    """
    Generates documentation with a clean 'uv' inspired UI.
    Detailed logic is captured in .doclify/logs/
    """
    logger.info("Starting documentation generation pipeline.")
    start_time = time.time()

    # 1. API Key Validation
    if not os.getenv("GOOGLE_API_KEY"):
        logger.error("GOOGLE_API_KEY is not set.")
        console.print("[bold red]✖ Error:[/bold red] [white]GOOGLE_API_KEY[/white] environment variable is not set.")
        return

    # 2. Config Validation
    config_path = Path("doclify.yaml")
    if not config_path.exists():
        logger.warning(f"Configuration file {config_path} missing.")
        console.print("[bold red]✖ Error:[/bold red] [blue]doclify.yaml[/blue] not found. Run [bold green]doclify init[/bold green] first.")
        return

    try:
        # Load Config
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        files = config.get("structure", [])
        
        if not files:
            logger.warning("No files found in doclify.yaml structure.")
            console.print("[bold yellow]⚠ Warning:[/bold yellow] No files found in [blue]doclify.yaml[/blue]")
            return

        # UV-style initial summary
        console.print(f"[bold cyan]Found[/bold cyan] [white]{len(files)} Files[/white] to Process")
        
        cache = load_cache()
        all_file_contents = []
        
        # 3. Reading Phase (Spinner disappears after)
        with console.status("[bold cyan]Reading[/bold cyan] project files...", spinner="dots"):
            for file_path in files:
                logger.debug(f"Extracting: {file_path}")
                content = extract_file_content(file_path)
                if not (content.startswith("Error") or content.startswith("File not found")):
                    all_file_contents.append((file_path, f"--- FILE: {file_path} ---\n{content}\n"))
                else:
                    logger.warning(f"Skipping {file_path}: {content[:50]}...")
            
            if not all_file_contents:
                logger.error("No valid file content found to process.")
                console.print("[bold yellow]⚠ Warning:[/bold yellow] No valid file content found to process.")
                return

        logger.info(f"Extracted content from {len(all_file_contents)} files. Starting summarization.")

        # 4. Summarization Phase (Count updates, spinner disappears after)
        batch_size = 5
        total_files = len(all_file_contents)
        
        with console.status(f"[bold cyan]Processing[/bold cyan] Files (0/{total_files})...", spinner="dots") as status:
            for i in range(0, total_files, batch_size):
                batch = all_file_contents[i:i + batch_size]
                batch_files = [item[0] for item in batch]
                batch_content = "\n".join([item[1] for item in batch])
                
                # Update console progress (minimalist style)
                current_progress = min(i + batch_size, total_files)
                status.update(f"[bold cyan]Processing[/bold cyan] Files ({current_progress}/{total_files})...")
                
                logger.info(f"Processing batch: {batch_files}")
                
                try:
                    batch_response = generate_doc(batch_content, type="batch_summary", json_format=FileSummaries)
                    
                    # Extract JSON
                    json_match = re.search(r'```json\s*(.*?)\s*```', batch_response, re.DOTALL)
                    new_summaries = json.loads(json_match.group(1)) if json_match else json.loads(batch_response.strip())
                    
                    if "files" not in cache:
                        cache["files"] = {}
                    cache["files"].update(new_summaries)
                    save_cache(cache)
                    
                except Exception as e:
                    logger.error(f"Error in batch {batch_files}: {str(e)}", exc_info=True)
                    continue

        # 5. Final README Generation
        generate_readme_file(cache, config)
        
        # Final success message with duration
        duration = time.time() - start_time
        console.print(f"[bold green]Generated[/bold green] README.md in [white]{duration:.1f} secs[/white]")
        logger.info(f"Pipeline completed successfully in {duration:.2f}s")

    except Exception as e:
        logger.critical(f"Pipeline failed: {str(e)}", exc_info=True)
        console.print(f"[bold red]✖ Failed[/bold red] to generate Documentation: {e}")