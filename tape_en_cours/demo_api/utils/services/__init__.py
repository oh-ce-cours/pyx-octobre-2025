"""
Services métier pour demo_api

Ce module contient les services qui encapsulent la logique métier :
- VMService : Gestion des VMs
- ReportService : Génération de rapports
"""
from .vm_service import VMService
from .report_service import ReportService

__all__ = ["VMService", "ReportService"]
