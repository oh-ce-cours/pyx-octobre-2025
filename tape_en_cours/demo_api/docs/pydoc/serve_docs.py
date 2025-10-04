#!/usr/bin/env python3
"""
Serveur HTTP simple pour servir la documentation pydoc.

Usage: python serve_docs.py [port]
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personnalisé pour servir les fichiers avec les bons types MIME."""
    
    def end_headers(self):
        # Ajouter des en-têtes CORS pour éviter les problèmes de sécurité
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def guess_type(self, path):
        """Définir le bon type MIME pour les fichiers."""
        mimetype, encoding = super().guess_type(path)
        if path.endswith('.html'):
            return 'text/html; charset=utf-8'
        elif path.endswith('.css'):
            return 'text/css; charset=utf-8'
        elif path.endswith('.js'):
            return 'application/javascript; charset=utf-8'
        return mimetype


def main():
    """Fonction principale du serveur."""
    # Définir le répertoire de travail
    docs_dir = Path(__file__).parent / "html"
    
    if not docs_dir.exists():
        print(f"❌ Erreur: Le répertoire {docs_dir} n'existe pas.")
        print("💡 Exécutez d'abord: python generate_pydoc.py")
        sys.exit(1)
    
    # Changer vers le répertoire de documentation
    os.chdir(docs_dir)
    
    # Port par défaut ou personnalisé
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    
    # Créer le serveur
    with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 Serveur de documentation pydoc démarré")
        print(f"📁 Répertoire servi: {docs_dir}")
        print(f"🌐 URL: http://localhost:{port}")
        print(f"📖 Index: http://localhost:{port}/index.html")
        print(f"🔧 Main: http://localhost:{port}/main.html")
        print("\n💡 Appuyez sur Ctrl+C pour arrêter le serveur")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n👋 Serveur arrêté")
            httpd.shutdown()


if __name__ == "__main__":
    main()
