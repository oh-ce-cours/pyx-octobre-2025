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
def create(
    path: str,
    max_length: int = 2,
    zip_name: str = "multiple_files.zip",
    output_txt: str = "short_named_python_files.txt",
) -> None:
    """Fonction principale pour exécuter le script."""
    p = Path(path)
    all_files = get_all_files(p)
    python_files = filter_python_files(all_files)
    short_named_files = filter_short_named_files(python_files, max_length)
    output_file_list(short_named_files, output_txt)


if __name__ == "__main__":
    app()
