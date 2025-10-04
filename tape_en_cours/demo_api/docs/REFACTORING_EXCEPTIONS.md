# Refactoring : Gestion d'erreurs avec des exceptions

## Résumé des changements

Ce refactoring remplace la gestion d'erreurs basée sur `return None` par un système d'exceptions robuste et explicite.

## Avantages du nouveau système

### ✅ Avant (avec `return None`)
```python
# Code difficile à déboguer
user = api.get_user_info()
if user is None:
    logger.error("Erreur inconnue")
    return
# Continuer avec user...
```

### ✅ Après (avec exceptions)
```python
# Code clair et explicite
try:
    user = api.get_user_info()
    # Continuer avec user...
except UserInfoError as e:
    logger.error(f"Erreur spécifique: {e}")
    # Gestion spécifique
except TokenError as e:
    logger.error(f"Problème de token: {e}")
    # Gestion spécifique
```

## Nouvelles exceptions créées

### `utils/api/exceptions.py`
- **`DemoAPIException`** : Exception de base pour toutes les erreurs API
- **`AuthenticationError`** : Erreurs d'authentification générales
- **`UserCreationError`** : Erreurs de création d'utilisateur
- **`UserLoginError`** : Erreurs de connexion utilisateur
- **`UserInfoError`** : Erreurs de récupération d'informations utilisateur
- **`UsersFetchError`** : Erreurs de récupération des utilisateurs
- **`VMsFetchError`** : Erreurs de récupération des VMs
- **`VMCreationError`** : Erreurs de création de VM
- **`TokenError`** : Erreurs liées aux tokens
- **`CredentialsError`** : Erreurs liées aux identifiants
- **`NetworkError`** : Erreurs réseau

## Fichiers modifiés

### 1. `utils/api/exceptions.py` (NOUVEAU)
Définit toutes les exceptions personnalisées avec des informations contextuelles riches.

### 2. `utils/api/auth.py`
- `create_user()` : Lève `UserCreationError` au lieu de `return None`
- `login_user()` : Lève `UserLoginError` au lieu de `return None`
- `get_logged_user_info()` : Lève `UserInfoError` ou `TokenError` au lieu de `return None`

### 3. `utils/api/vm.py`
- `get_vms()` : Lève `VMsFetchError` au lieu de `return None`
- `create_vm()` : Lève `VMCreationError` au lieu de `return None`

### 4. `utils/api/user.py`
- `get_users()` : Lève `UsersFetchError` au lieu de `return None`

### 5. `utils/api/__init__.py`
- Mise à jour des signatures de méthodes pour refléter les nouvelles exceptions
- Suppression des `Optional` dans les types de retour
- Gestion des exceptions dans `create_authenticated_client()`

### 6. `utils/password_utils.py`
- `get_or_create_token()` : Lève `CredentialsError` ou `TokenError` au lieu de `return None`

### 7. `main.py`
- Ajout de blocs `try/except` pour gérer les nouvelles exceptions
- Gestion spécifique de chaque type d'erreur
- Messages d'erreur plus informatifs

## Exemples d'utilisation

### Récupération des utilisateurs
```python
try:
    users = api.users.get()
    logger.info(f"Récupéré {len(users)} utilisateurs")
except UsersFetchError as e:
    logger.error(f"Impossible de récupérer les utilisateurs: {e}")
    users = []
```

### Création d'une VM
```python
try:
    vm = api.users.create_vm(
        user_id=user["id"],
        name="Ma VM",
        operating_system="Ubuntu 22.04",
        cpu_cores=2,
        ram_gb=4,
        disk_gb=50
    )
    logger.info(f"VM créée: {vm['id']}")
except VMCreationError as e:
    logger.error(f"Échec création VM: {e}")
```

### Authentification
```python
try:
    token = get_or_create_token(base_url, email, password)
    api.set_token(token)
except CredentialsError as e:
    logger.error(f"Identifiants invalides: {e}")
except TokenError as e:
    logger.error(f"Erreur de token: {e}")
```

## Test du refactoring

Un script de test `test_exceptions.py` a été créé pour vérifier que toutes les exceptions sont correctement levées.

```bash
python test_exceptions.py
```

## Migration depuis l'ancien code

### Ancien code
```python
user = api.get_user_info()
if user is None:
    logger.error("Erreur")
    return
```

### Nouveau code
```python
try:
    user = api.get_user_info()
except UserInfoError as e:
    logger.error(f"Erreur spécifique: {e}")
    return
```

## Avantages du refactoring

1. **Clarté** : Les erreurs sont explicites et typées
2. **Débogage** : Stack traces complètes avec contexte
3. **Robustesse** : Gestion d'erreurs spécifique par type
4. **Maintenabilité** : Code plus facile à comprendre et maintenir
5. **Documentation** : Les exceptions documentent les cas d'erreur possibles
6. **Sécurité** : Pas de valeurs `None` inattendues dans le code

## Prochaines étapes recommandées

1. Tester le refactoring avec des données réelles
2. Ajouter des tests unitaires pour chaque exception
3. Documenter les cas d'usage spécifiques
4. Considérer l'ajout de retry logic pour les erreurs réseau
5. Implémenter des métriques d'erreurs pour le monitoring
