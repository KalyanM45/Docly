import yaml
import click
from pathlib import Path
from rich.console import Console
from doclify.utils.scanner import scan_repo
from doclify.utils.logger import get_logger

logger = get_logger(__name__)
console = Console()

def refresh_project():
    """
    Refreshes the doclify.yaml configuration by re-scanning the repository.
    """
    config_path = Path("doclify.yaml")
    
    if not config_path.exists():
        logger.warning(f"Refresh failed: {config_path} not found.")
        console.print("[bold red]✖ Error:[/bold red] [blue]doclify.yaml[/blue] not found. Please run [bold green]doclify init[/bold green] first.")
        return

    logger.info(f"Refresh sequence started. Directory: {Path.cwd()}")

    try:        
        repo_structure = scan_repo()
        logger.info(f"Scan complete. Found {len(repo_structure.get('structure', []))} file nodes.")
            
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(repo_structure, f, default_flow_style=False)
        logger.info(f"Configuration refreshed in {config_path}")

    except Exception as e:
        logger.error(f"Refresh failed: {str(e)}", exc_info=True)
        console.print(f"[bold red]✖ Error:[/bold red] Failed to refresh project. Check logs in [blue].doclify/logs/[/blue]")
        return

    console.print(f"[bold green]Refreshed[/bold green] [blue]doclify.yaml[/blue]")    
    logger.info(f"Refresh process completed successfully.")