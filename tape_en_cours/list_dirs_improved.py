from pathlib import Path


def get_all_files(p):
    return [x for x in p.rglob("*") if x.is_file()]
