"""
Services métier pour demo_api

Ce module contient les services qui encapsulent la logique métier :
- VMService : Gestion des VMs
- ReportService : Génération de rapports
- DataManager : Gestion centralisée des données
"""

from .vm_service import VMService
from .report_service import ReportService
from .data_manager import DataManager

__all__ = ["VMService", "ReportService", "DataManager"]
