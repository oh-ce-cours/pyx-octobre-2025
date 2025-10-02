from pathlib import Path

import typer

from list_dirs_improved import (
    filter_python_files,
    get_all_files,
    filter_short_named_files,
    generate_zip_archive,
    output_file_list,
)


app = typer.Typer()


@app.command()
def create(path: str = ".") -> None:
    """Fonction principale pour exécuter le script."""
    p = Path(".")
    all_files = get_all_files(p)
    python_files = filter_python_files(all_files)
    short_named_files = filter_short_named_files(python_files, 2)
    output_file_list(short_named_files, "short_named_python_files.txt")


if __name__ == "__main__":
    create()
