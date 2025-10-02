from pathlib import Path
import json
import typer

from list_dirs_improved import (
    filter_python_files,
    get_all_files,
    filter_short_named_files,
    generate_zip_archive,
    generate_tar_archive,
    output_file_list,
)

app = typer.Typer()


@app.command()
def archive(
    path: str,
    max_length: int = 2,
    archive_name: str = "multiple_files.zip",
    archive_format: str = "zip",
) -> None:
    """Crée une archive (zip ou tar) des fichiers Python avec des noms courts."""
    p = Path(path)
    all_files = get_all_files(p)
    python_files = filter_python_files(all_files)
    short_named_files = filter_short_named_files(python_files, max_length)
    if archive_format.lower() == "tar":
        generate_tar_archive(short_named_files, archive_name)
    else:
        generate_zip_archive(short_named_files, archive_name)


@app.command()
def report(
    path: str,
    max_length: int = 2,
    output_txt: str = "short_named_python_files.txt",
) -> None:
    """Génère un rapport texte des fichiers Python avec des noms courts."""
    p = Path(path)
    all_files = get_all_files(p)
    python_files = filter_python_files(all_files)
    short_named_files = filter_short_named_files(python_files, max_length)
    output_file_list(short_named_files, output_txt)
    json.dump([str(f) for f in short_named_files], open("report.json", "w"), indent=4)


if __name__ == "__main__":
    app()
