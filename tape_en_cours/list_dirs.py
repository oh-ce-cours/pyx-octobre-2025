# print([x for x in p.iterdir() if x.is_dir()])

# on peut lister les fichiers récursivement et prendre uniquement les fichiers qui
# ont un nom d'une longueur supérieure à 4 caractères
#
#
# et les zipper dans compressed.zip

import zipfile

p = zipfile.Path(".")
files_to_zip = []
for x in p.rglob("*.py"):
    if x.is_file() and len(x.stem) < 2:
        files_to_zip.append(x)
print(files_to_zip)

with zipfile.ZipFile("multiple_files.zip", mode="w") as archive:
    for filename in files_to_zip:
        archive.write(filename, arcname=filename.name)
