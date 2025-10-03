import subprocess
import shlex
import logging

# Configuration du logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# File handler pour les erreurs uniquement
file_handler = logging.FileHandler("plop.log")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
file_handler.setLevel(logging.WARNING)
logger.addHandler(file_handler)

# Stream handler pour tous les niveaux
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


try:
    result = subprocess.run(
        shlex.split("python archive.py report .. --output-txt toto.txt"),
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout
    logging.debug("Résultat de ls :")
    logging.info(output)
    logging.info(result.stderr)
    logging.info("returncode: %s", result.returncode)
except subprocess.CalledProcessError as e:
    logging.error("Erreur lors de l'exécution de ls: %s", e)
    logging.error("Sortie d'erreur : %s", e.stderr)
except Exception as e:
    logging.critical("Une erreur inattendue est survenue : %s", e)
