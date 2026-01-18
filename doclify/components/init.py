import yaml
import click
from pathlib import Path
from rich.console import Console
from doclify.utils.scanner import scan_repo
from doclify.utils.logger import get_logger

logger = get_logger(__name__)
console = Console()

def init_project():
    """
    Initialize or reinitialize a Doclify project.
    """
    config_path = Path("doclify.yaml")
    is_reinit = config_path.exists()
    
    logger.info(f"Init sequence started. Directory: {Path.cwd()}")

    try:        
        with console.status("[bold cyan]Analyzing[/bold cyan] repository structure...", spinner="dots"):
            repo_structure = scan_repo()
            logger.info(f"Scan complete. Found {len(repo_structure.get('structure', []))} file nodes.")
            
        gitignore_path = Path(".gitignore")
        doclify_ignore = ".doclify/\n"
        
        if gitignore_path.exists():
            content = gitignore_path.read_text(encoding="utf-8")
            if ".doclify/" not in content:
                logger.info("Appending .doclify/ to existing .gitignore")
                # Ensure we start on a new line if file isn't empty and doesn't end with newline
                prefix = "" if not content or content.endswith("\n") else "\n"
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    f.write(prefix + doclify_ignore)
        else:
            logger.info("Creating new .gitignore with .doclify/")
            gitignore_path.write_text(doclify_ignore, encoding="utf-8")

        with console.status("[bold cyan]Writing[/bold cyan] configuration...", spinner="dots"):
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(repo_structure, f, default_flow_style=False)
            logger.info(f"Configuration written to {config_path}")

    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}", exc_info=True)
        console.print(f"[bold red]✖ Error:[/bold red] Failed to initialize project. Check logs in [blue].doclify/logs/[/blue]")
        return

    action = "Reinitialized" if is_reinit else "Initialized"
    console.print(f"[bold green]✔ {action}[/bold green] [blue]doclify.yaml[/blue]")
    console.print(f"\n[bold cyan]Next steps[/bold cyan]")
    console.print(f"  • Review [blue]doclify.yaml[/blue] to customize included files")
    console.print(f"  • Run [bold green]doclify run[/bold green] to generate documentation")
    
    logger.info(f"Init process completed successfully.")