"""
Générateur de rapports Markdown pour demo_api
"""

import os
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .base import BaseReportGenerator
from utils.logging_config import get_logger

logger = get_logger(__name__)


class MarkdownReportGenerator(BaseReportGenerator):
    """Générateur de rapports au format Markdown avec templates Jinja2"""

    def __init__(self, output_directory: str = "outputs"):
        """
        Initialise le générateur de rapports Markdown

        Args:
            output_directory: Dossier de sortie pour les rapports Markdown
        """
        super().__init__(output_directory)
        self.markdown_directory = os.path.join(output_directory, "markdown")
        self._ensure_markdown_directory()

        # Configuration de Jinja2
        template_dir = os.path.join(
            os.path.dirname(__file__), "..", "templates", "markdown"
        )
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Ajout de filtres personnalisés
        self.jinja_env.filters["pad"] = self._pad_filter

    def _ensure_markdown_directory(self) -> None:
        """Crée le dossier Markdown s'il n'existe pas"""
        if not os.path.exists(self.markdown_directory):
            os.makedirs(self.markdown_directory, exist_ok=True)
            logger.info(f"Dossier Markdown créé: {self.markdown_directory}")

    def _pad_filter(self, text: str, width: int) -> str:
        """Filtre Jinja2 pour padding de texte"""
        return text.ljust(width)

    def get_extension(self) -> str:
        """Retourne l'extension des fichiers Markdown"""
        return "md"

    def generate(
        self,
        data: Any,
        filename: Optional[str] = None,
        template_name: str = "default.md.j2",
    ) -> str:
        """
        Génère un rapport Markdown

        Args:
            data: Données à inclure dans le rapport Markdown
            filename: Nom de fichier personnalisé (optionnel)
            template_name: Nom du template Jinja2 à utiliser

        Returns:
            str: Chemin vers le fichier Markdown généré
        """
        if filename is None:
            filename = self._generate_filename("report", self.get_extension())
        else:
            # S'assurer que le fichier a la bonne extension
            if not filename.endswith(f".{self.get_extension()}"):
                filename = f"{filename}.{self.get_extension()}"
            filename = os.path.join(self.markdown_directory, filename)

        # Préparer les données avec métadonnées
        report_data = {"metadata": self._get_metadata(), "data": data}

        # Générer le fichier Markdown
        try:
            template = self.jinja_env.get_template(template_name)
            content = template.render(**report_data)

            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(
                "Rapport Markdown généré avec succès",
                filename=filename,
                template=template_name,
            )

            return filename

        except Exception as e:
            logger.error(
                "Erreur lors de la génération du rapport Markdown",
                filename=filename,
                error=str(e),
            )
            raise

    def generate_users_vms_report(
        self, users: List[Dict[str, Any]], filename: str = "vm_users.md"
    ) -> str:
        """
        Génère un rapport spécifique pour les utilisateurs et VMs

        Args:
            users: Liste des utilisateurs avec leurs VMs associées
            filename: Nom du fichier de sortie

        Returns:
            str: Chemin vers le fichier généré
        """
        logger.info(
            "Génération du rapport utilisateurs/VMs Markdown",
            users_count=len(users),
            filename=filename,
        )

        # Statistiques supplémentaires
        stats = self._calculate_users_vms_stats(users)

        report_data = {
            "summary": {
                "total_users": len(users),
                "total_vms": stats["total_vms"],
                "vms_by_status": stats["vms_by_status"],
                "users_with_vms": stats["users_with_vms"],
                "users_without_vms": stats["users_without_vms"],
            },
            "users": users,
        }

        return self.generate(report_data, filename, "users_vms_report.md.j2")

    def generate_status_report(
        self, status_data: Dict[str, Any], filename: str = "vm_status_report.md"
    ) -> str:
        """
        Génère un rapport de statut des VMs

        Args:
            status_data: Données de statut des VMs
            filename: Nom du fichier de sortie

        Returns:
            str: Chemin vers le fichier généré
        """
        logger.info("Génération du rapport de statut Markdown", filename=filename)

        return self.generate(status_data, filename, "vm_status_report.md.j2")

    def _calculate_users_vms_stats(self, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcule les statistiques des utilisateurs et VMs"""
        total_vms: int = 0
        vms_by_status: Dict[str, int] = {}
        users_with_vms: int = 0
        users_without_vms: int = 0

        for user in users:
            user_vms = user.get("vms", [])
            if user_vms:
                users_with_vms += 1
                total_vms += len(user_vms)

                # Compter les VMs par statut
                for vm in user_vms:
                    status = vm.get("status", "unknown")
                    vms_by_status[status] = vms_by_status.get(status, 0) + 1
            else:
                users_without_vms += 1

        return {
            "total_vms": total_vms,
            "vms_by_status": vms_by_status,
            "users_with_vms": users_with_vms,
            "users_without_vms": users_without_vms,
        }
