from pathlib import Path

p = Path(".")
# print([x for x in p.iterdir() if x.is_dir()])

# on peut lister les fichiers récursivement et prendre uniquement les fichiers qui
# ont un nom d'une longueur supérieure à 4 caractères
#
#
# et les zipper dans compressed.zip

for x in p.rglob("*"):
    if x.is_file() and len(x.stem) < 4:
        print(x)
