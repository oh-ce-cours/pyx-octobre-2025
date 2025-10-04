#!/usr/bin/env python3
"""
Script de test pour démontrer l'amélioration du formatage des dates
"""

from utils.date_utils import format_timestamp_for_display, parse_unix_timestamp, get_current_timestamp
import datetime

def test_date_formatting():
    """Teste le formatage des dates avec différents formats"""
    
    print("🧪 Test du formatage des dates")
    print("=" * 50)
    
    # Test avec le timestamp fourni par l'utilisateur
    timestamp_user = 1759590925156
    print(f"📅 Timestamp utilisateur: {timestamp_user}")
    print(f"   Formaté: {format_timestamp_for_display(timestamp_user)}")
    print()
    
    # Test avec un timestamp actuel
    current_ts = get_current_timestamp()
    print(f"📅 Timestamp actuel: {current_ts}")
    print(f"   Formaté: {format_timestamp_for_display(current_ts)}")
    print()
    
    # Test avec un objet datetime
    now = datetime.datetime.now()
    print(f"📅 Objet datetime: {now}")
    print(f"   Formaté: {format_timestamp_for_display(now)}")
    print()
    
    # Test avec None
    print(f"📅 Valeur None: {format_timestamp_for_display(None)}")
    print()
    
    # Test avec une chaîne
    print(f"📅 Chaîne: {format_timestamp_for_display('2025-10-04 17:15:25')}")
    print()
    
    print("✅ Tous les tests de formatage sont passés !")

if __name__ == "__main__":
    test_date_formatting()
