#!/usr/bin/env python3
"""
Serveur pdoc3 pour la documentation moderne.

Usage: python serve_pdoc3.py [port]
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Démarre le serveur pdoc3."""
    # Port par défaut
    port = sys.argv[1] if len(sys.argv) > 1 else 8080
    
    print("🚀 Démarrage du serveur pdoc3")
    print(f"🌐 URL: http://localhost:{port}")
    print("💡 Appuyez sur Ctrl+C pour arrêter")
    
    try:
        # Commande pdoc3 pour servir la documentation
        subprocess.run([
            "pdoc", "--http", f":{port}",
            "main", "report_manager", "utils.config"
        ])
    except KeyboardInterrupt:
        print("\n👋 Serveur arrêté")
    except FileNotFoundError:
        print("❌ pdoc3 n'est pas installé. Installez-le avec :")
        print("pip install pdoc3")


if __name__ == "__main__":
    main()
