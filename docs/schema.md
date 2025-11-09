# Database Schema (Multi-Organization Model)

This schema defines the **multi-tenant B2B architecture**, where a single user can belong to multiple organizations and hold roles at both the **organization** and **team** levels.

---

## ER Diagram : [**View on dbdocs.io →**](https://dbdocs.io/Jerin%20Sam/intsea-models)  

## Overview

- **Organizations**
  - Represent tenant companies using the platform.  
  - Each organization is an isolated workspace with its own users, teams, and data.  
  - One organization can have multiple teams.  
  - One organization can have multiple users linked through `OrganizationMemberships`.

- **Users**
  - Global entities identified by a unique email.  
  - A user can belong to multiple organizations.  
  - A user can also be part of multiple teams across different organizations.  
  - User-to-organization relationships are managed through `OrganizationMemberships`.  
  - User-to-team relationships are managed through `TeamUserRoles`.

- **OrganizationMemberships**
  - Links users ↔ organizations.  
  - Defines the user’s organization-level role (e.g., `org_admin`, `member`, `viewer`).  
  - Includes a boolean `is_default` flag to mark the user’s default organization.  
  - One user can have multiple memberships, but only one default organization.

- **Teams**
  - Belong to a single organization.  
  - Used to group users by project, department, or purpose.  
  - Each team can include multiple users through `TeamUserRoles`.  
  - Supports fine-grained access control at the team level.

- **TeamUserRoles**
  - Links users ↔ teams.  
  - Assigns one or more roles per user per team.  
  - Enables flexible role combinations (e.g., a user can be a “manager” in one team and a “viewer” in another).  
  - References reusable `Roles` defined in the system.

- **Roles**
  - Defines reusable permission sets that can apply to both organizations and teams.  
  - Core roles include `org_admin`, `member`, `viewer`, and `team_manager`.  
  - Designed for scalability — new roles can be added without structural changes.  
  - Shared between org-level and team-level entities for consistent RBAC management.


---

## ER Diagram

**View Live Diagram:**  
[**View on dbdocs.io →**](https://dbdocs.io/Jerin%20Sam/intsea-models)  


---

