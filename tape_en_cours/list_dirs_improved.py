from pathlib import Path


def get_all_files(path):
    return [x for x in path.rglob("*") if x.is_file()]


def filter_python_files(files):
    res = []
    for file in files:
        if file.suffix == ".py":
            res.append(file)
    return res


def filter_short_named_files(files, max_length):
    return [f for f in files if len(f.stem) < max_length]


def output_file_list(files, output_path):
    with open(output_path, "w") as f:
        for file in files:
            f.write(str(file) + "\n")


p = Path(".")
all_files = get_all_files(p)
python_files = filter_python_files(all_files)
print(python_files)
