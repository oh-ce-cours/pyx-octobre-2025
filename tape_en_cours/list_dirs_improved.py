from pathlib import Path


def get_all_files(path: Path) -> list[Path]:
    return [x for x in path.rglob("*") if x.is_file()]


def filter_python_files(files: list[Path]) -> list[Path]:
    res = []
    for file in files:
        if file.suffix == ".py":
            res.append(file)
    return res


def filter_short_named_files(files: list[Path], max_length):
    return [f for f in files if len(f.stem) < max_length]


def output_file_list(files, output_path):
    with open(output_path, "w", encoding="utf8") as f:
        for file in files:
            f.write(str(file) + "\n")


p = Path(".")
all_files = get_all_files(p)
python_files = filter_python_files(all_files)
short_named_files = filter_short_named_files(python_files, 2)
output_file_list(short_named_files, "short_named_python_files.txt")
