import subprocess
import csv

users = [
    {"firstname": "John", "lastname": "Smith", "username": "jsmith", "password": "Pa55word!", "ou": "Pupils"},
    {"firstname": "Jane", "lastname": "Doe", "username": "jdoe", "password": "Pa55word!", "ou": "Teachers"},
    {"firstname": "Bob", "lastname": "Jones", "username": "bjones", "password": "Pa55word!", "ou": "AdminStaff"},
]

for user in users:
    ou_path = f"OU={user['ou']},OU=School,DC=assignment2,DC=local"
    ps_command = f"""
New-ADUser `
    -Name "{user['firstname']} {user['lastname']}" `
    -GivenName "{user['firstname']}" `
    -Surname "{user['lastname']}" `
    -SamAccountName "{user['username']}" `
    -UserPrincipalName "{user['username']}@assignment2.local" `
    -Path "{ou_path}" `
    -AccountPassword (ConvertTo-SecureString "{user['password']}" -AsPlainText -Force) `
    -Enabled $true
"""
    result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Created user: {user['username']}")
    else:
        print(f"Failed: {user['username']} — {result.stderr.strip()}")
