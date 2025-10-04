"""
Module de génération de données factices avec Faker.
Génère des données réalistes pour les utilisateurs et les machines virtuelles.
"""

import random
import unicodedata
from datetime import datetime, timedelta
from typing import List, Dict, Any
from faker import Faker
from faker.providers import internet, company, lorem, date_time

from utils.logging_config import get_logger

# Logger pour ce module
logger = get_logger(__name__)

# Initialisation de Faker avec la locale française
fake = Faker("fr_FR")
fake.add_provider(internet)
fake.add_provider(company)
fake.add_provider(lorem)
fake.add_provider(date_time)


class VMDataGenerator:
    """Générateur de données pour les machines virtuelles."""

    # Systèmes d'exploitation réalistes
    OPERATING_SYSTEMS = [
        "Ubuntu 22.04 LTS",
        "Ubuntu 20.04 LTS",
        "CentOS 8",
        "Red Hat Enterprise Linux 8",
        "Windows Server 2022",
        "Windows Server 2019",
        "Debian 11",
        "SUSE Linux Enterprise Server 15",
        "AlmaLinux 8",
        "Rocky Linux 8",
        "Fedora 38",
        "openSUSE Leap 15.4",
    ]

    # Statuts possibles des VMs
    VM_STATUSES = ["running", "stopped", "paused", "provisioning", "deleting"]

    # Probabilités de statut (plus réalistes)
    STATUS_PROBABILITIES = {
        "running": 0.6,  # 60% des VMs sont en cours d'exécution
        "stopped": 0.25,  # 25% sont arrêtées
        "paused": 0.05,  # 5% sont en pause
        "provisioning": 0.05,  # 5% sont en cours de création
        "deleting": 0.05,  # 5% sont en cours de suppression
    }

    @classmethod
    def generate_vm_name(cls) -> str:
        """Génère un nom réaliste pour une VM."""
        prefixes = [
            "web",
            "db",
            "app",
            "api",
            "cache",
            "monitor",
            "backup",
            "test",
            "dev",
            "prod",
        ]
        suffix = fake.word().capitalize()
        return f"{random.choice(prefixes)}-{suffix}"

    @classmethod
    def generate_cpu_cores(cls) -> int:
        """Génère un nombre réaliste de cœurs CPU."""
        # Distribution réaliste : plus de VMs avec peu de cœurs
        weights = [0.3, 0.4, 0.2, 0.1]  # 1-2, 4, 8, 16+ cœurs
        ranges = [(1, 2), (4, 4), (8, 8), (16, 32)]
        range_choice = random.choices(ranges, weights=weights)[0]
        return random.randint(range_choice[0], range_choice[1])

    @classmethod
    def generate_ram_gb(cls) -> int:
        """Génère une quantité réaliste de RAM."""
        # Distribution réaliste : plus de VMs avec peu de RAM
        weights = [0.2, 0.3, 0.3, 0.2]  # 2-4, 8, 16, 32+ GB
        ranges = [(2, 4), (8, 8), (16, 16), (32, 128)]
        range_choice = random.choices(ranges, weights=weights)[0]
        return random.randint(range_choice[0], range_choice[1])

    @classmethod
    def generate_disk_gb(cls) -> int:
        """Génère une taille réaliste de disque."""
        # Distribution réaliste : plus de VMs avec des disques moyens
        weights = [0.1, 0.4, 0.3, 0.2]  # 20-50, 100, 200, 500+ GB
        ranges = [(20, 50), (100, 100), (200, 200), (500, 2000)]
        range_choice = random.choices(ranges, weights=weights)[0]
        return random.randint(range_choice[0], range_choice[1])

    @classmethod
    def generate_status(cls) -> str:
        """Génère un statut réaliste basé sur les probabilités."""
        return random.choices(
            list(cls.STATUS_PROBABILITIES.keys()),
            weights=list(cls.STATUS_PROBABILITIES.values()),
        )[0]

    @classmethod
    def generate_vm(cls, user_id: int, vm_id: int) -> Dict[str, Any]:
        """Génère une VM complète avec des données réalistes."""
        # Date de création dans les 6 derniers mois
        created_at = fake.date_time_between(start_date="-6M", end_date="now")

        vm_data = {
            "id": vm_id,
            "user_id": user_id,
            "name": cls.generate_vm_name(),
            "operating_system": random.choice(cls.OPERATING_SYSTEMS),
            "cpu_cores": cls.generate_cpu_cores(),
            "ram_gb": cls.generate_ram_gb(),
            "disk_gb": cls.generate_disk_gb(),
            "status": cls.generate_status(),
            "created_at": created_at,
        }

        logger.debug("VM générée", vm_id=vm_id, user_id=user_id, name=vm_data["name"])
        return vm_data


class UserDataGenerator:
    """Générateur de données pour les utilisateurs."""

    # Domaines d'entreprise réalistes
    COMPANY_DOMAINS = [
        "gmail.com",
        "outlook.com",
        "yahoo.com",
        "hotmail.com",
        "company.com",
        "entreprise.fr",
        "corp.com",
        "business.org",
        "tech.io",
        "startup.com",
        "innovation.fr",
        "digital.net",
    ]

    @classmethod
    def generate_email(cls, name: str) -> str:
        """Génère un email réaliste basé sur le nom."""
        # Nettoyer le nom pour l'email : supprimer les accents et caractères spéciaux
        # Normaliser les caractères Unicode
        normalized = unicodedata.normalize("NFD", name.lower())
        # Supprimer les caractères diacritiques (accents)
        clean_name = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
        # Remplacer les espaces par des points et supprimer autres caractères spéciaux
        clean_name = clean_name.replace(" ", ".").replace("-", "").replace("'", "")
        # Garder seulement les caractères alphanumériques et les points
        clean_name = "".join(c for c in clean_name if c.isalnum() or c == ".")

        domain = random.choice(cls.COMPANY_DOMAINS)
        return f"{clean_name}@{domain}"

    @classmethod
    def generate_user(cls, user_id: int) -> Dict[str, Any]:
        """Génère un utilisateur complet avec des données réalistes."""
        # Générer un nom français réaliste
        name = fake.name()

        # Date de création dans les 12 derniers mois
        created_at = fake.date_time_between(start_date="-12M", end_date="now")

        user_data = {
            "id": user_id,
            "name": name,
            "email": cls.generate_email(name),
            "created_at": created_at,
            "vms": [],  # Les VMs seront ajoutées séparément
        }

        logger.debug(
            "Utilisateur généré", user_id=user_id, name=name, email=user_data["email"]
        )
        return user_data


class DataGenerator:
    """Générateur principal pour créer des datasets complets."""

    @classmethod
    def generate_users_with_vms(
        cls, user_count: int = 50, vm_per_user_range: tuple = (0, 5)
    ) -> List[Dict[str, Any]]:
        """
        Génère un dataset complet d'utilisateurs avec leurs VMs.

        Args:
            user_count: Nombre d'utilisateurs à générer
            vm_per_user_range: Tuple (min, max) du nombre de VMs par utilisateur

        Returns:
            Liste des utilisateurs avec leurs VMs associées
        """
        logger.info(
            "Génération du dataset", user_count=user_count, vm_range=vm_per_user_range
        )

        users = []
        vm_counter = 1

        for user_id in range(1, user_count + 1):
            # Générer l'utilisateur
            user = UserDataGenerator.generate_user(user_id)

            # Générer les VMs pour cet utilisateur
            vm_count = random.randint(vm_per_user_range[0], vm_per_user_range[1])
            user_vms = []

            for _ in range(vm_count):
                vm = VMDataGenerator.generate_vm(user_id, vm_counter)
                user_vms.append(vm)
                vm_counter += 1

            user["vms"] = user_vms
            users.append(user)

            logger.debug(
                "Utilisateur généré avec VMs",
                user_id=user_id,
                vm_count=vm_count,
                user_name=user["name"],
            )

        total_vms = sum(len(user["vms"]) for user in users)
        logger.info(
            "Dataset généré avec succès",
            total_users=len(users),
            total_vms=total_vms,
            avg_vms_per_user=total_vms / len(users) if users else 0,
        )

        return users

    @classmethod
    def generate_vms_only(
        cls, vm_count: int, user_ids: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Génère uniquement des VMs pour des utilisateurs existants.

        Args:
            vm_count: Nombre de VMs à générer
            user_ids: Liste des IDs d'utilisateurs existants

        Returns:
            Liste des VMs générées
        """
        logger.info(
            "Génération de VMs", vm_count=vm_count, available_users=len(user_ids)
        )

        vms = []
        for vm_id in range(1, vm_count + 1):
            user_id = random.choice(user_ids)
            vm = VMDataGenerator.generate_vm(user_id, vm_id)
            vms.append(vm)

        logger.info("VMs générées avec succès", count=len(vms))
        return vms
