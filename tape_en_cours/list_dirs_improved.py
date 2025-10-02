"""Maniuplation de fichiers et de répertoires avec pathlib et zipfile."""

from pathlib import Path
import zipfile
import tarfile


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
    """Filtre les fichiers dont le nom est plus court qu'une longueur maximale.

    :param files: Liste des fichiers à filtrer
    :type files: list[Path]
    :param max_length: Longueur maximale du nom du fichier (sans extension)
    :type max_length: int
    :return: Liste des fichiers avec un nom court
    :rtype: list[Path]
    """
    return [f for f in files if len(f.stem) < max_length]


def output_file_list(files: list[Path], output_path_name: str) -> None:
    """Écrit la liste des fichiers dans un fichier texte.

    :param files: Liste des fichiers à écrire
    :type files: list[Path]
    :param output_path_name: Nom du fichier de sortie
    :type output_path_name: str
    :return: None
    :rtype: None
    """
    with open(output_path_name, "w", encoding="utf8") as f:
        for file in files:
            f.write(str(file) + "\n")


def generate_zip_archive(files: list[Path], zip_name: str) -> None:
    """Crée une archive zip contenant les fichiers spécifiés.

    :param files: Liste des fichiers à archiver
    :type files: list[Path]
    :param zip_name: Nom de l'archive zip à créer
    :type zip_name: str
    :return: None
    :rtype: None
    """
    with zipfile.ZipFile(zip_name, mode="w") as archive:
        for filename in files:
            archive.write(filename, arcname=filename.name)


def generate_tar_archive(files: list[Path], tar_name: str) -> None:
    """Crée une archive tar.gz contenant les fichiers spécifiés.

    :param files: Liste des fichiers à archiver
    :type files: list[Path]
    :param tar_name: Nom de l'archive tar.gz à créer
    :type tar_name: str
    :return: None
    :rtype: None
    """
    try:
        with tarfile.open(tar_name, mode="x:gz") as archive:
            for filename in files:
                archive.add(filename, arcname=filename.name)
    except FileExistsError, OSError:
        print(f"L'archive {tar_name} existe déjà. Choisissez un autre nom.")
    except Exception as e:
        print(
            f"Une erreur est survenue lors de la création de l'archive tar: {e}",
            type(e),
        )


def main() -> None:
    """Fonction principale pour exécuter le script."""
    print("dans main de list_dirs_improved")
    p = Path(".")
    all_files = get_all_files(p)
    python_files = filter_python_files(all_files)
    short_named_files = filter_short_named_files(python_files, 2)
    # output_file_list(short_named_files, "short_named_python_files.txt")
    generate_zip_archive(short_named_files, "multiple_files.zip")


if __name__ == "__main__":
    main()
