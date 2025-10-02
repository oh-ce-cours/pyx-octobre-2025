"""Maniuplation de fichiers et de répertoires avec pathlib et zipfile."""

from pathlib import Path
import zipfile


def get_all_files(path: Path) -> list[Path]:
    """Récupère tous les fichiers d'un répertoire de manière récursive.

    :param path: Le chemin du répertoire à parcourir
    :type path: Path
    :return: Liste des chemins de tous les fichiers trouvés
    :rtype: list[Path]
    """
    return [x for x in path.rglob("*") if x.is_file()]


def filter_python_files(files: list[Path]) -> list[Path]:
    """Filtre une liste de fichiers pour ne garder que les fichiers Python.

    :param files: Liste des fichiers à filtrer
    :type files: list[Path]
    :return: Liste des fichiers Python
    :rtype: list[Path]
    """
    res = []
    for file in files:
        if file.suffix == ".py":
            res.append(file)
    return res


def filter_short_named_files(files: list[Path], max_length: int) -> list[Path]:
    return [f for f in files if len(f.stem) < max_length]


def output_file_list(files: list[Path], output_path_name: str) -> None:
    with open(output_path_name, "w", encoding="utf8") as f:
        for file in files:
            f.write(str(file) + "\n")


def generate_zip_archive(files: list[Path], zip_name: str) -> None:
    with zipfile.ZipFile(zip_name, mode="w") as archive:
        for filename in files:
            archive.write(filename, arcname=filename.name)


p = Path(".")
all_files = get_all_files(p)
python_files = filter_python_files(all_files)
short_named_files = filter_short_named_files(python_files, 2)
# output_file_list(short_named_files, "short_named_python_files.txt")
generate_zip_archive(short_named_files, "multiple_files.zip")
