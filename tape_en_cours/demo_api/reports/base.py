"""
Classe de base pour tous les générateurs de rapports
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
from utils.logging_config import get_logger

logger = get_logger(__name__)


class BaseReportGenerator(ABC):
    """Classe de base abstraite pour tous les générateurs de rapports"""
    
    def __init__(self, output_directory: str = "outputs"):
        """
        Initialise le générateur de rapport
        
        Args:
            output_directory: Dossier de sortie pour les rapports
        """
        self.output_directory = output_directory
        self._ensure_output_directory()
    
    def _ensure_output_directory(self) -> None:
        """Crée le dossier de sortie s'il n'existe pas"""
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory, exist_ok=True)
            logger.info(f"Dossier de sortie créé: {self.output_directory}")
    
    def _generate_filename(self, base_name: str, extension: str, timestamp: bool = True) -> str:
        """
        Génère un nom de fichier avec timestamp optionnel
        
        Args:
            base_name: Nom de base du fichier
            extension: Extension du fichier
            timestamp: Ajouter un timestamp au nom
            
        Returns:
            str: Nom de fichier complet
        """
        if timestamp:
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{base_name}_{timestamp_str}.{extension}"
        else:
            filename = f"{base_name}.{extension}"
        
        return os.path.join(self.output_directory, filename)
    
    def _get_metadata(self) -> Dict[str, Any]:
        """Retourne les métadonnées du rapport"""
        return {
            "generated_at": datetime.now().isoformat(),
            "generator": self.__class__.__name__,
            "version": "1.0.0"
        }
    
    @abstractmethod
    def generate(self, data: Any, filename: Optional[str] = None) -> str:
        """
        Génère un rapport
        
        Args:
            data: Données à inclure dans le rapport
            filename: Nom de fichier personnalisé (optionnel)
            
        Returns:
            str: Chemin vers le fichier généré
        """
        pass
    
    @abstractmethod
    def get_extension(self) -> str:
        """
        Retourne l'extension des fichiers générés par ce rapport
        
        Returns:
            str: Extension (ex: "json", "html", "md")
        """
        pass
