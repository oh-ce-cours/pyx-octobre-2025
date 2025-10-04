"""
Générateur de rapports JSON pour demo_api
"""

import json
import os
from typing import Dict, Any, List, Optional
from .base import BaseReportGenerator
from utils.logging_config import get_logger

logger = get_logger(__name__)


class JSONReportGenerator(BaseReportGenerator):
    """Générateur de rapports au format JSON"""
    
    def __init__(self, output_directory: str = "outputs"):
        """
        Initialise le générateur de rapports JSON
        
        Args:
            output_directory: Dossier de sortie pour les rapports JSON
        """
        super().__init__(output_directory)
        self.json_directory = os.path.join(output_directory, "json")
        self._ensure_json_directory()
    
    def _ensure_json_directory(self) -> None:
        """Crée le dossier JSON s'il n'existe pas"""
        if not os.path.exists(self.json_directory):
            os.makedirs(self.json_directory, exist_ok=True)
            logger.info(f"Dossier JSON créé: {self.json_directory}")
    
    def get_extension(self) -> str:
        """Retourne l'extension des fichiers JSON"""
        return "json"
    
    def generate(self, data: Any, filename: Optional[str] = None) -> str:
        """
        Génère un rapport JSON
        
        Args:
            data: Données à inclure dans le rapport JSON
            filename: Nom de fichier personnalisé (optionnel)
            
        Returns:
            str: Chemin vers le fichier JSON généré
        """
        if filename is None:
            filename = self._generate_filename("report", self.get_extension())
        else:
            # S'assurer que le fichier a la bonne extension
            if not filename.endswith(f".{self.get_extension()}"):
                filename = f"{filename}.{self.get_extension()}"
            filename = os.path.join(self.json_directory, filename)
        
        # Préparer les données avec métadonnées
        report_data = {
            "metadata": self._get_metadata(),
            "data": data
        }
        
        # Générer le fichier JSON
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    report_data,
                    f,
                    indent=4,
                    sort_keys=True,
                    default=str,
                    ensure_ascii=False
                )
            
            logger.info(
                "Rapport JSON généré avec succès",
                filename=filename,
                data_size=len(str(data))
            )
            
            return filename
            
        except Exception as e:
            logger.error(
                "Erreur lors de la génération du rapport JSON",
                filename=filename,
                error=str(e)
            )
            raise
    
    def generate_users_vms_report(self, users: List[Dict[str, Any]], filename: str = "vm_users.json") -> str:
        """
        Génère un rapport spécifique pour les utilisateurs et VMs
        
        Args:
            users: Liste des utilisateurs avec leurs VMs associées
            filename: Nom du fichier de sortie
            
        Returns:
            str: Chemin vers le fichier généré
        """
        logger.info(
            "Génération du rapport utilisateurs/VMs",
            users_count=len(users),
            filename=filename
        )
        
        # Statistiques supplémentaires
        stats = self._calculate_users_vms_stats(users)
        
        report_data = {
            "summary": {
                "total_users": len(users),
                "total_vms": stats["total_vms"],
                "vms_by_status": stats["vms_by_status"],
                "users_with_vms": stats["users_with_vms"],
                "users_without_vms": stats["users_without_vms"]
            },
            "users": users
        }
        
        return self.generate(report_data, filename)
    
    def _calculate_users_vms_stats(self, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcule les statistiques des utilisateurs et VMs"""
        total_vms = 0
        vms_by_status = {}
        users_with_vms = 0
        users_without_vms = 0
        
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
            "users_without_vms": users_without_vms
        }
    
    def generate_api_summary_report(self, api_data: Dict[str, Any], filename: str = "api_summary.json") -> str:
        """
        Génère un rapport de résumé de l'API
        
        Args:
            api_data: Données de l'API (utilisateurs, VMs, etc.)
            filename: Nom du fichier de sortie
            
        Returns:
            str: Chemin vers le fichier généré
        """
        logger.info("Génération du rapport de résumé API", filename=filename)
        
        summary_data = {
            "api_info": {
                "base_url": api_data.get("base_url", "unknown"),
                "timestamp": api_data.get("timestamp", "unknown"),
                "status": "success"
            },
            "counts": {
                "users": len(api_data.get("users", [])),
                "vms": len(api_data.get("vms", []))
            },
            "raw_data": api_data
        }
        
        return self.generate(summary_data, filename)
