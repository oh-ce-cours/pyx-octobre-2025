"""
Module de génération de rapports pour demo_api

Ce module contient tous les générateurs de rapports :
- JSON : Rapports structurés pour l'API
- HTML : Rapports web interactifs
- Markdown : Documentation et rapports texte
- CSV : Données tabulaires
"""

from .json_reports import JSONReportGenerator
from .base import BaseReportGenerator

__all__ = ["JSONReportGenerator", "BaseReportGenerator"]
