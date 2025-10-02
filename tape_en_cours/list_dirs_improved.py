from pathlib import Path


def get_all_files(path):
    return [x for x in path.rglob("*") if x.is_file()]


p = Path(".")
all_files = get_all_files(p)
print(all_files)
