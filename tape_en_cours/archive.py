from pathlib import Path


def main() -> None:
    """Fonction principale pour exécuter le script."""
    p = Path(".")
    all_files = get_all_files(p)
    python_files = filter_python_files(all_files)
    short_named_files = filter_short_named_files(python_files, 2)
    # output_file_list(short_named_files, "short_named_python_files.txt")
    generate_zip_archive(short_named_files, "multiple_files.zip")
