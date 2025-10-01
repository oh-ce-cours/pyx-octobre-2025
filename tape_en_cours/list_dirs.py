p = Path(".")
[x for x in p.iterdir() if x.is_dir()]
