from pathlib import Path

p = Path(".")
print([x for x in p.iterdir() if x.is_dir()])
