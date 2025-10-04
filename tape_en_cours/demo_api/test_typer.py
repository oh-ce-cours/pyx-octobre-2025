#!/usr/bin/env python3
"""Test simple de Typer"""

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def test():
    """Test de Typer fonctionnel"""
    console.print("[bold green]✅ Typer fonctionne correctement ![/bold green]")


if __name__ == "__main__":
    app()
