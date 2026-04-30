# Enterprise School Network Infrastructure — Active Directory & Security Lab

> A full end-to-end Windows Server network deployment simulating a real-world primary school IT environment. Covers identity management, internet security, endpoint deployment, monitoring, and disaster recovery.

---

## Overview

Designed and deployed a multi-server enterprise network from scratch, replicating the infrastructure a school IT department would run. The environment enforces role-based access control, web content filtering, automated software deployment, and 24/7 server monitoring — all integrated within a Windows Active Directory domain.

---

## Technologies & Tools Used

| Category | Tools |
|---|---|
| Identity & Directory | Windows Server AD DS, Group Policy (GPO), LDAP |
| DNS & DHCP | Windows DNS Server, DHCP with static reservations |
| Web Security | Squid Web Proxy, Web Filtering (whitelist/blacklist), ICAP Server |
| Monitoring | Nagios XI |
| Deployment | WDS (PXE Boot), SCCM, AD Software Deployment, Python scripting |
| Remote Access | VPN, RDP (role-restricted) |
| Backup | Automated daily server backups over VPN |
| Scripting | Python (bulk user import via CSV) |
| Networking | NAT, dual NIC configuration |

---

## Architecture

```
                        [Internet - 8.8.8.8]
                               |
                         [NAT Gateway]
                               |
                        [Squid Proxy / ICAP]
                               |
            ┌──────────────────┴──────────────────┐
            │                                     │
       [PDC - 10.0.1.2]                   [BDC - 10.0.1.10]
     assignment2.local               assignment2-bdc.local
       DNS | DHCP | AD                  AD Replication
            │
    ┌───────┴────────┐
    │                │
[Clients]       [Nagios XI]
Pupils/Teachers/  Monitoring
  Admin/SysAdmin
```

**Domain:** `assignment2.local`  
**Subnet:** `10.0.0.0/24`

---

## Features Implemented

### Active Directory & Identity Management

- **PDC + BDC** — Primary and Backup Domain Controllers configured with full AD replication, ensuring high availability
- **DNS** — Forward and reverse lookup zones created; DNS relay configured to `8.8.8.8` for external resolution
- **DHCP** — Scope configured with all servers statically reserved by MAC address
- **User Groups** — Four role-based groups: `Pupils`, `Teachers`, `Administrative Staff`, `System Administrators`
- **Group Policy** — Custom GPOs applied per group:
  - Pupils: blocked `.exe` and `.msi` execution, write-protected system paths
  - Teachers/Staff: standard restrictions with elevated privileges where required
- **Roaming Profiles** — Profile paths and home directories mapped to a central network share, following users across machines
- **Bulk User Import** — Python script reads from a `.csv` file and automatically provisions AD accounts with correct group membership

### Internet Access & Web Security

- **NAT** — Configured internet access for the internal network via NAT; verified with successful pings to `8.8.8.8`
- **Web Proxy** — Squid proxy deployed; all client traffic routed through it — direct internet access blocked
- **Content Filtering:**
  - Pupils filtered via **whitelist** — can only access pre-approved sites
  - Teachers and staff filtered via **blacklist** — unrestricted except blocked categories
- **LDAP-Authenticated Proxy** — Proxy authenticates against AD via LDAP, preventing users from bypassing filters by switching accounts
- **Deep Packet Inspection** — ICAP server deployed for keyword-based content filtering at the packet level

### Endpoint Deployment

- **WDS / PXE Boot** — Windows Deployment Services configured; machines boot from network and auto-join the domain
- **Image Locking** — Deployment images tied to specific physical machines (MAC-based enforcement)
- **AD Software Deployment** — Applications (Chrome, LibreOffice via script fallback) deployed automatically via GPO on login
- **Role-Based App Deployment** — Software packages distributed based on user group membership

### Monitoring (Nagios XI)

- **Server Health** — All servers monitored for uptime and availability
- **Disk Space Alerts** — Warning triggered at 80% usage; critical alert at 90%
- **Service Checks** — Active monitors for PDC, BDC, DNS, and DHCP services
- **Login Auditing** — GPO configured to log all logon events: username, machine name, and timestamp
- **Web Access Logging** — Proxy access logs integrated into Nagios audit trail with timestamps
- **Access Control** — Only `Administrator` account has access to the Nagios dashboard

### Extras & Hardening

- **Daily Backups** — Automated nightly server backups scheduled to an internal backup machine
- **VPN** — VPN tunnel configured to external endpoint; backup traffic transmitted over VPN
- **RDP (Admin)** — Remote Desktop enabled on all machines, restricted to `System Administrators` only
- **Teacher VPN** — Per-teacher VPN accounts provisioned to allow remote access to network drives and resources
- **Teacher RDP** — Teachers can RDP into their school desktop from home; pupil accounts explicitly blocked from RDP

---

## Python User Import Script

Bulk-created Active Directory user accounts from a `.csv` file, automatically assigning each user to the correct group based on their role column.

```python
# Reads from users.csv → creates AD accounts → assigns group membership
# Fields: FirstName, LastName, Role, Username, Password
```

> Script stored in the repository under `/scripts/import_users.py`

---

## Repository Structure

```
📦 school-network-lab/
├── 📄 README.md
├── 📁 scripts/
│   └── import_users.py        # Bulk AD user creation from CSV
├── 📁 screenshots/            # Evidence screenshots organised by section
│   ├── ad-setup/
│   ├── dhcp-dns/
│   ├── web-filtering/
│   ├── monitoring/
│   ├── deployment/
│   └── extras/
└── 📁 configs/
    └── notes.md               # Key IPs, domain names, config references
```

---

## Skills Demonstrated

- Windows Server administration and Active Directory architecture
- DNS, DHCP, and network topology design
- Web proxy configuration and multi-tier content filtering
- LDAP integration for proxy authentication
- Automated user provisioning with Python
- Network monitoring with alerting thresholds (Nagios XI)
- PXE/WDS network boot and image deployment
- Group Policy design for security hardening
- VPN and RDP configuration with role-based access
- Backup strategy design and implementation

---

## Notes

- All credentials shown are lab/test credentials only — not used in any production environment
- This project was completed as part of a university networking module (CO2516) and extended with additional hardening features
- Some features (SCCM, full PXE image locking) proved more challenging to fully implement and are something I plan to revisit and complete in the future
