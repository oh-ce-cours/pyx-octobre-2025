import requests
from utils.date_utils import parse_unix_timestamp


def get_users(base_url):
    resp = requests.get(f"{base_url}/user", timeout=5)
    resp.raise_for_status()
    users = []
    for user in resp.json():
        user["created_at"] = parse_unix_timestamp(user["created_at"])
        users.append(user)
    return users


def add_vms_to_users(users, vms):
    for user in users:
        user_id = user["id"]
        user_vms = []
        for vm in vms:
            user_vm_id = vm["user_id"]
            if user_vm_id == user_id:
                user_vms.append(vm)
        user["vms"] = user_vms
