"""
Service de génération de rapports
"""

from typing import Dict, Any, List, Optional
from utils.api import Api
from utils.logging_config import get_logger
from reports import JSONReportGenerator, MarkdownReportGenerator, HTMLReportGenerator

logger = get_logger(__name__)


class ReportService:
    """Service pour la génération de rapports"""

    def __init__(self, api_client: Api):
        """
        Initialise le service de rapport

        Args:
            api_client: Client API unifié
        """
        self.api = api_client


    def generate_users_vms_report(
        self, users: List[Dict[str, Any]], vms: List[Dict[str, Any]], filename: str = "vm_users.json"
    ) -> Optional[str]:
        """
        Génère un rapport utilisateurs/VMs

        Args:
            users: Liste des utilisateurs
            vms: Liste des VMs
            filename: Nom du fichier de sortie

        Returns:
            Chemin du fichier généré ou None si échec
        """
        logger.info("Début de génération du rapport utilisateurs/VMs")

        if not users or not vms:
            logger.warning(
                "Impossible de générer le rapport: données manquantes",
                users_count=len(users),
                vms_count=len(vms),
            )
            return None

        # Associer les VMs aux utilisateurs
        self.api.users.add_vms_to_users(users, vms)

        # Génération du rapport JSON
        try:
            logger.info("Génération du rapport JSON")
            json_generator = JSONReportGenerator()
            report_file = json_generator.generate_users_vms_report(users, filename)
            logger.info("Rapport JSON généré avec succès", filename=report_file)
            return report_file
        except (IOError, TypeError) as e:
            logger.error("Erreur lors de la génération du rapport", error=str(e))
            return None

    def generate_status_report(
        self, users: List[Dict[str, Any]], vms: List[Dict[str, Any]], filename: str = "vm_status_report.json"
    ) -> Optional[str]:
        """
        Génère un rapport des VMs par statut

        Args:
            users: Liste des utilisateurs
            vms: Liste des VMs
            filename: Nom du fichier de sortie

        Returns:
            Chemin du fichier généré ou None si échec
        """
        logger.info("Début de génération du rapport de statut des VMs")

        if not vms:
            logger.warning(
                "Impossible de générer le rapport de statut: pas de VMs disponibles"
            )
            return None

        # Compter les VMs par statut
        status_counts: Dict[str, int] = {}
        for vm in vms:
            status = vm.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        # Créer le rapport avec une structure claire et concise
        status_report = {
            "summary": {
                "total_vms": len(vms),
                "total_users": len(users),
            },
            "vm_status_counts": status_counts,
        }

        try:
            json_generator = JSONReportGenerator()
            report_file = json_generator.generate(status_report, filename)
            logger.info("Rapport de statut généré avec succès", filename=report_file)
            return report_file
        except (IOError, TypeError) as e:
            logger.error(
                "Erreur lors de la génération du rapport de statut", error=str(e)
            )
            return None

    def generate_users_vms_report_markdown(
        self, users: List[Dict[str, Any]], vms: List[Dict[str, Any]], filename: str = "vm_users.md"
    ) -> Optional[str]:
        """
        Génère un rapport utilisateurs/VMs en Markdown

        Args:
            users: Liste des utilisateurs
            vms: Liste des VMs
            filename: Nom du fichier de sortie

        Returns:
            Chemin du fichier généré ou None si échec
        """
        logger.info("Début de génération du rapport utilisateurs/VMs Markdown")

        if not users or not vms:
            logger.warning(
                "Impossible de générer le rapport: données manquantes",
                users_count=len(users),
                vms_count=len(vms),
            )
            return None

        # Associer les VMs aux utilisateurs
        self.api.users.add_vms_to_users(users, vms)

        # Génération du rapport Markdown
        try:
            logger.info("Génération du rapport Markdown")
            markdown_generator = MarkdownReportGenerator()
            report_file = markdown_generator.generate_users_vms_report(users, filename)
            logger.info("Rapport Markdown généré avec succès", filename=report_file)
            return report_file
        except (IOError, TypeError) as e:
            logger.error(
                "Erreur lors de la génération du rapport Markdown", error=str(e)
            )
            return None

    def generate_users_vms_report_html(
        self, users: List[Dict[str, Any]], vms: List[Dict[str, Any]], filename: str = "vm_users.html"
    ) -> Optional[str]:
        """
        Génère un rapport utilisateurs/VMs en HTML

        Args:
            users: Liste des utilisateurs
            vms: Liste des VMs
            filename: Nom du fichier de sortie

        Returns:
            Chemin du fichier généré ou None si échec
        """
        logger.info("Début de génération du rapport utilisateurs/VMs HTML")

        if not users or not vms:
            logger.warning(
                "Impossible de générer le rapport: données manquantes",
                users_count=len(users),
                vms_count=len(vms),
            )
            return None

        # Associer les VMs aux utilisateurs
        self.api.users.add_vms_to_users(users, vms)

        # Génération du rapport HTML
        try:
            logger.info("Génération du rapport HTML")
            html_generator = HTMLReportGenerator()
            report_file = html_generator.generate_users_vms_report(users, filename)
            logger.info("Rapport HTML généré avec succès", filename=report_file)
            return report_file
        except (IOError, TypeError) as e:
            logger.error("Erreur lors de la génération du rapport HTML", error=str(e))
            return None

    def generate_status_report_markdown(
        self, users: List[Dict[str, Any]], vms: List[Dict[str, Any]], filename: str = "vm_status_report.md"
    ) -> Optional[str]:
        """
        Génère un rapport de statut des VMs en Markdown

        Args:
            users: Liste des utilisateurs
            vms: Liste des VMs
            filename: Nom du fichier de sortie

        Returns:
            Chemin du fichier généré ou None si échec
        """
        logger.info("Début de génération du rapport de statut des VMs Markdown")

        if not vms:
            logger.warning(
                "Impossible de générer le rapport de statut: pas de VMs disponibles"
            )
            return None

        # Compter les VMs par statut
        status_counts: Dict[str, int] = {}
        for vm in vms:
            status = vm.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        # Créer le rapport avec une structure claire et concise
        status_report = {
            "summary": {
                "total_vms": len(vms),
                "total_users": len(users),
            },
            "vm_status_counts": status_counts,
        }

        try:
            markdown_generator = MarkdownReportGenerator()
            report_file = markdown_generator.generate_status_report(
                status_report, filename
            )
            logger.info(
                "Rapport de statut Markdown généré avec succès", filename=report_file
            )
            return report_file
        except (IOError, TypeError) as e:
            logger.error(
                "Erreur lors de la génération du rapport de statut Markdown",
                error=str(e),
            )
            return None

    def generate_status_report_html(
        self, users: List[Dict[str, Any]], vms: List[Dict[str, Any]], filename: str = "vm_status_report.html"
    ) -> Optional[str]:
        """
        Génère un rapport de statut des VMs en HTML

        Args:
            users: Liste des utilisateurs
            vms: Liste des VMs
            filename: Nom du fichier de sortie

        Returns:
            Chemin du fichier généré ou None si échec
        """
        logger.info("Début de génération du rapport de statut des VMs HTML")

        if not vms:
            logger.warning(
                "Impossible de générer le rapport de statut: pas de VMs disponibles"
            )
            return None

        # Compter les VMs par statut
        status_counts: Dict[str, int] = {}
        for vm in vms:
            status = vm.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        # Créer le rapport avec une structure claire et concise
        status_report = {
            "summary": {
                "total_vms": len(vms),
                "total_users": len(users),
            },
            "vm_status_counts": status_counts,
        }

        try:
            html_generator = HTMLReportGenerator()
            report_file = html_generator.generate_status_report(status_report, filename)
            logger.info(
                "Rapport de statut HTML généré avec succès", filename=report_file
            )
            return report_file
        except (IOError, TypeError) as e:
            logger.error(
                "Erreur lors de la génération du rapport de statut HTML", error=str(e)
            )
            return None
