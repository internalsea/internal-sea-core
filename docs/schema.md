# Database Schema (Multi-Organization Model)

This schema defines the **multi-tenant B2B architecture**, where a single user can belong to multiple organizations and hold roles at both the **organization** and **team** levels.

---

## Overview

- **Organizations** represent tenant companies using the platform.  
- **Users** are global (unique email across all orgs) and can be a part of multiple orgs.
- **OrganizationMemberships** link users ↔ organizations with optional org-level roles.  
- **Teams** belong to a single organization.  
- **TeamUserRoles** link users ↔ teams with team-level roles.  
- **Roles** defines reusable role definitions shared across orgs and teams.  



---

## ER Diagram

**View Live Diagram:**  
[**View on dbdocs.io →**](https://dbdocs.io/Jerin%20Sam/intsea-models)  


---

