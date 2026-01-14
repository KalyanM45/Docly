from pathlib import Path
import pathspec

def load_gitignore_patterns(ignore_name=None):
    patterns = []

    if ignore_name:
        builtin_dir = Path(__file__).resolve().parent / "gitignores"
        ignore_file = builtin_dir / f"{ignore_name}.gitignore"
        if ignore_file.exists():
            patterns.extend(ignore_file.read_text().splitlines())

    project_gitignore = Path("data/Python.gitignore")
    if project_gitignore.exists():
        patterns.extend(project_gitignore.read_text().splitlines())

    return patterns


def scan_repo(ignore_name=None):
    spec = pathspec.PathSpec.from_lines(
        "gitwildmatch",
        load_gitignore_patterns(ignore_name)
    )

    files = [
        str(p)
        for p in Path(".").rglob("*")
        if p.is_file() and not spec.match_file(p) and p.suffix == ".py" or p.suffix == ".md" or p.suffix == ".txt"
    ]

    return {
        "project": Path.cwd().name,
        "structure": files
    }