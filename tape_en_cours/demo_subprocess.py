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
    logging.info("Résultat de ls :")
    logging.info(output)
    logging.info(result.stderr)
    logging.info("returncode:", result.returncode)
except subprocess.CalledProcessError as e:
    logging.error(f"Erreur lors de l'exécution de ls: {e}")
    logging.error(f"Sortie d'erreur : {e.stderr}")
except Exception as e:
    logging.critical(f"Une erreur inattendue est survenue : {e}")
print("coucou")
