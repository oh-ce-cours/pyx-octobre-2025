import subprocess
import shlex
import logging

try:
    result = subprocess.run(
        shlex.split("python archive.py report .. --output-txt toto.txt"),
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout
    print("Résultat de ls :")
    print(output)
    print(result.stderr)
    print("returncode:", result.returncode)
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution de ls: {e}")
    print(f"Sortie d'erreur : {e.stderr}")
except Exception as e:
    print(f"Une erreur inattendue est survenue : {e}")
