"""
Service de génération de rapports
"""

from typing import Dict, Any, List, Optional
from utils.api import Api
from utils.api.exceptions import UsersFetchError, VMsFetchError
from utils.logging_config import get_logger
from reports import JSONReportGenerator

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
    
    def fetch_data(self) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Récupère les données des utilisateurs et VMs depuis l'API
        
        Returns:
            Tuple contenant (users, vms) ou ([], []) en cas d'erreur
        """
        logger.info("Début de récupération des données pour rapport")
        
        # Récupération des utilisateurs
        try:
            users = self.api.users.get()
            logger.info("Utilisateurs récupérés", count=len(users))
        except UsersFetchError as e:
            logger.error("Impossible de récupérer les utilisateurs", error=str(e))
            users = []
        
        # Récupération des VMs
        try:
            vms = self.api.vms.get()
            logger.info("VMs récupérées", count=len(vms))
        except VMsFetchError as e:
            logger.error("Impossible de récupérer les VMs", error=str(e))
            vms = []
        
        return users, vms
    
    def generate_users_vms_report(self, filename: str = "vm_users.json") -> Optional[str]:
        """
        Génère un rapport utilisateurs/VMs
        
        Args:
            filename: Nom du fichier de sortie
            
        Returns:
            Chemin du fichier généré ou None si échec
        """
        logger.info("Début de génération du rapport utilisateurs/VMs")
        
        # Récupérer les données
        users, vms = self.fetch_data()
        
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
        except Exception as e:
            logger.error("Erreur lors de la génération du rapport", error=str(e))
            return None
    
    def generate_status_report(self, filename: str = "vm_status_report.json") -> Optional[str]:
        """
        Génère un rapport des VMs par statut
        
        Args:
            filename: Nom du fichier de sortie
            
        Returns:
            Chemin du fichier généré ou None si échec
        """
        logger.info("Début de génération du rapport de statut des VMs")
        
        # Récupérer les données
        users, vms = self.fetch_data()
        
        if not vms:
            logger.warning("Impossible de générer le rapport de statut: pas de VMs disponibles")
            return None
        
        # Compter les VMs par statut
        status_counts = {}
        for vm in vms:
            status = vm.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Créer le rapport
        status_report = {
            "metadata": {
                "generated_at": "now",  # Le générateur ajoutera le timestamp
                "total_vms": len(vms),
                "total_users": len(users)
            },
            "vm_status_summary": status_counts
        }
        
        try:
            json_generator = JSONReportGenerator()
            report_file = json_generator.generate(status_report, filename)
            logger.info("Rapport de statut généré avec succès", filename=report_file)
            return report_file
        except Exception as e:
            logger.error("Erreur lors de la génération du rapport de statut", error=str(e))
            return None
