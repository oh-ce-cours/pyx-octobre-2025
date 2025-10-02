# print([x for x in p.iterdir() if x.is_dir()])

# on peut lister les fichiers récursivement et prendre uniquement les fichiers qui
# ont un nom d'une longueur supérieure à 4 caractères
#
#
# et les zipper dans compressed.zip

"""Regarde les fichiers .py dans le répertoire courant et ses sous-répertoires
et zippe ceux dont le nom (sans l'extension) est plus court que 2
caractères dans un fichier multiple_files.zip
"""

from pathlib import Path
import zipfile

p = Path(".")
files_to_zip = []
for file in p.rglob("*.py"):
    if file.is_file() and len(file.stem) < 2:
        files_to_zip.append(file)
print(files_to_zip)

with zipfile.ZipFile("multiple_files.zip", mode="w") as archive:
    for filename in files_to_zip:
        archive.write(filename, arcname=filename.name)

smtp.send(files_to_zip)


def mon_nom_de_fonction(nb):
    for i in range(nb):
        print("coucou")


mon_nom_de_fonction("toto")
