"""Static demo seed data for local development."""

from __future__ import annotations

from typing import Any, TypedDict


class CapabilitySeed(TypedDict):
    name: str
    description: str


class TeamSeed(TypedDict):
    name: str
    description: str


class PersonSeed(TypedDict):
    full_name: str
    email: str
    role_title: str
    seniority_level: str
    team: str
    capability: str
    availability_percent: int
    location: str
    is_active: bool


class BusinessDomainSeed(TypedDict):
    name: str
    description: str
    owner_email: str


class ProjectSeed(TypedDict, total=False):
    name: str
    description: str
    project_type: str
    status: str
    client_name: str
    account_name: str
    owner_email: str
    team: str
    capability: str
    start_date_offset_days: int
    target_end_date_offset_days: int
    budget_amount: str
    budget_currency: str
    priority: str
    health_status: str
    delivery_notes: str


class DataProductSeed(TypedDict, total=False):
    name: str
    description: str
    type: str
    status: str
    quality_status: str
    business_domain: str
    business_owner_email: str
    technical_owner_email: str
    capability: str
    team: str
    refresh_frequency: str
    source_systems: str
    consumers: str
    documentation_url: str


class RelationshipSeed(TypedDict, total=False):
    source_type: str
    source_key: str
    target_type: str
    target_key: str
    link_type: str
    title: str
    description: str


class WorkItemSeed(TypedDict, total=False):
    title: str
    description: str
    type: str
    status: str
    priority: str
    assignee_email: str
    reporter_email: str
    project: str
    data_product: str | None
    capability: str
    team: str
    due_date_offset_days: int
    estimate_points: int


class FileStorageSeed(TypedDict, total=False):
    name: str
    storage_type: str
    base_url: str
    description: str
    is_active: bool


class CompliancePolicySeed(TypedDict, total=False):
    name: str
    description: str
    status: str
    owner_email: str
    version: str


class ComplianceRuleSeed(TypedDict, total=False):
    policy: str
    code: str
    name: str
    description: str
    severity: str
    subject_type: str


class ComplianceControlSeed(TypedDict, total=False):
    rule_code: str
    name: str
    description: str
    control_type: str
    status: str
    frequency: str


class ComplianceCheckSeed(TypedDict, total=False):
    title: str
    description: str
    subject_type: str
    subject_key: str
    rule_code: str
    control_name: str
    status: str
    check_type: str
    result_summary: str
    evidence_file: str
    due_date_offset_days: int


class FileAssetSeed(TypedDict, total=False):
    name: str
    description: str
    file_type: str
    status: str
    sensitivity: str
    external_url: str
    version: str
    storage: str
    entity_type: str
    entity_key: str
    purpose: str
    is_evidence: bool
    evidence_type: str


CAPABILITIES: list[CapabilitySeed] = [
    {
        "name": "Data Engineering",
        "description": (
            "Builds and operates data pipelines, data products, integrations and platform services."
        ),
    },
    {
        "name": "BI",
        "description": (
            "Builds dashboards, reports, semantic models and business-facing analytics."
        ),
    },
    {
        "name": "AI",
        "description": (
            "Builds AI assistants, automation, prompt workflows and intelligent product features."
        ),
    },
    {
        "name": "CloudOps",
        "description": (
            "Manages cloud infrastructure, deployments, monitoring, cost and platform reliability."
        ),
    },
    {
        "name": "Data Governance",
        "description": (
            "Owns data quality, documentation, policies, compliance and stewardship processes."
        ),
    },
    {
        "name": "Product Management",
        "description": (
            "Defines product vision, roadmap, priorities, user needs and delivery outcomes."
        ),
    },
    {
        "name": "Business Analysis",
        "description": (
            "Translates business needs into requirements, use cases, process flows "
            "and acceptance criteria."
        ),
    },
    {
        "name": "Architecture",
        "description": (
            "Defines solution architecture, integration patterns, technical standards "
            "and cross-domain design."
        ),
    },
]

TEAMS: list[TeamSeed] = [
    {
        "name": "Core Platform Team",
        "description": "Builds Internal Sea and shared platform capabilities.",
    },
    {
        "name": "Data Products Team",
        "description": "Owns business data products, dashboards, datasets and metric layers.",
    },
    {
        "name": "Governance Team",
        "description": "Owns compliance, documentation, quality checks and policy implementation.",
    },
    {
        "name": "AI Enablement Team",
        "description": "Builds AI features, assistants, automation and productivity tooling.",
    },
    {
        "name": "Delivery Operations Team",
        "description": (
            "Tracks project delivery, team capacity, risks, decisions and operating metrics."
        ),
    },
]

PEOPLE: list[PersonSeed] = [
    {
        "full_name": "Nikita Rogatov",
        "email": "nikita@example.com",
        "role_title": "Partner, Data Engineering and Cloud",
        "seniority_level": "partner",
        "team": "Core Platform Team",
        "capability": "Architecture",
        "availability_percent": 70,
        "location": "Netherlands",
        "is_active": True,
    },
    {
        "full_name": "Sofia Marin",
        "email": "sofia.marin@example.com",
        "role_title": "Product Owner",
        "seniority_level": "lead",
        "team": "Core Platform Team",
        "capability": "Product Management",
        "availability_percent": 80,
        "location": "Netherlands",
        "is_active": True,
    },
    {
        "full_name": "Daniel Weber",
        "email": "daniel.weber@example.com",
        "role_title": "Data Architect",
        "seniority_level": "principal",
        "team": "Data Products Team",
        "capability": "Architecture",
        "availability_percent": 60,
        "location": "Germany",
        "is_active": True,
    },
    {
        "full_name": "Maya Singh",
        "email": "maya.singh@example.com",
        "role_title": "Data Engineer",
        "seniority_level": "senior",
        "team": "Data Products Team",
        "capability": "Data Engineering",
        "availability_percent": 90,
        "location": "Portugal",
        "is_active": True,
    },
    {
        "full_name": "Lucas Ferreira",
        "email": "lucas.ferreira@example.com",
        "role_title": "BI Lead",
        "seniority_level": "lead",
        "team": "Data Products Team",
        "capability": "BI",
        "availability_percent": 75,
        "location": "Portugal",
        "is_active": True,
    },
    {
        "full_name": "Emma Johnson",
        "email": "emma.johnson@example.com",
        "role_title": "Data Governance Lead",
        "seniority_level": "lead",
        "team": "Governance Team",
        "capability": "Data Governance",
        "availability_percent": 80,
        "location": "United States",
        "is_active": True,
    },
    {
        "full_name": "Omar Haddad",
        "email": "omar.haddad@example.com",
        "role_title": "AI Engineer",
        "seniority_level": "senior",
        "team": "AI Enablement Team",
        "capability": "AI",
        "availability_percent": 85,
        "location": "Netherlands",
        "is_active": True,
    },
    {
        "full_name": "Anna Kowalski",
        "email": "anna.kowalski@example.com",
        "role_title": "CloudOps Engineer",
        "seniority_level": "senior",
        "team": "Core Platform Team",
        "capability": "CloudOps",
        "availability_percent": 65,
        "location": "Poland",
        "is_active": True,
    },
    {
        "full_name": "Grace Lee",
        "email": "grace.lee@example.com",
        "role_title": "Business Analyst",
        "seniority_level": "medior",
        "team": "Delivery Operations Team",
        "capability": "Business Analysis",
        "availability_percent": 95,
        "location": "United Kingdom",
        "is_active": True,
    },
    {
        "full_name": "Tom Becker",
        "email": "tom.becker@example.com",
        "role_title": "Junior Data Engineer",
        "seniority_level": "junior",
        "team": "Data Products Team",
        "capability": "Data Engineering",
        "availability_percent": 100,
        "location": "Germany",
        "is_active": True,
    },
]

BUSINESS_DOMAINS: list[BusinessDomainSeed] = [
    {
        "name": "Finance",
        "description": (
            "Financial reporting, planning, budget tracking, margin analysis "
            "and management reporting."
        ),
        "owner_email": "emma.johnson@example.com",
    },
    {
        "name": "Sales",
        "description": (
            "Sales performance, customer demand, sell-through, revenue and commercial reporting."
        ),
        "owner_email": "lucas.ferreira@example.com",
    },
    {
        "name": "Product",
        "description": (
            "Product master data, assortment, categories, attributes and product lifecycle."
        ),
        "owner_email": "daniel.weber@example.com",
    },
    {
        "name": "Inventory",
        "description": (
            "Stock position, availability, replenishment, warehouse and inventory health."
        ),
        "owner_email": "maya.singh@example.com",
    },
    {
        "name": "Customer",
        "description": ("Customer segmentation, behavior, retention, loyalty and personalization."),
        "owner_email": "sofia.marin@example.com",
    },
    {
        "name": "Operations",
        "description": (
            "Delivery operations, capacity, project execution, risks, decisions and performance."
        ),
        "owner_email": "grace.lee@example.com",
    },
]

CLIENT_PROJECTS: list[ProjectSeed] = [
    {
        "name": "Finance Data Platform Migration",
        "project_type": "client_project",
        "status": "active",
        "client_name": "Example Retail Group",
        "account_name": "Retail Analytics",
        "owner_email": "nikita@example.com",
        "team": "Data Products Team",
        "capability": "Data Engineering",
        "start_date_offset_days": -30,
        "target_end_date_offset_days": 90,
        "budget_amount": "180000",
        "budget_currency": "EUR",
        "priority": "high",
        "health_status": "warning",
        "delivery_notes": (
            "Migration scope is clear, but reconciliation and ownership require attention."
        ),
    },
    {
        "name": "Executive Reporting Foundation",
        "project_type": "client_project",
        "status": "active",
        "client_name": "Example Fashion Group",
        "account_name": "Executive Analytics",
        "owner_email": "lucas.ferreira@example.com",
        "team": "Data Products Team",
        "capability": "BI",
        "start_date_offset_days": -15,
        "target_end_date_offset_days": 45,
        "budget_amount": "90000",
        "budget_currency": "EUR",
        "priority": "medium",
        "health_status": "healthy",
        "delivery_notes": "First dashboard scope is aligned with business stakeholders.",
    },
    {
        "name": "AI Governance Pilot",
        "project_type": "pilot",
        "status": "planned",
        "client_name": "Example Holding",
        "account_name": "AI Governance",
        "owner_email": "emma.johnson@example.com",
        "team": "Governance Team",
        "capability": "Data Governance",
        "start_date_offset_days": 7,
        "target_end_date_offset_days": 60,
        "budget_amount": "65000",
        "budget_currency": "EUR",
        "priority": "high",
        "health_status": "unknown",
        "delivery_notes": "Pilot will define policies, rules, evidence and AI tool controls.",
    },
]

INTERNAL_PROJECTS: list[ProjectSeed] = [
    {
        "name": "Internal Sea MVP",
        "project_type": "internal_project",
        "status": "active",
        "owner_email": "nikita@example.com",
        "team": "Core Platform Team",
        "capability": "Product Management",
        "start_date_offset_days": -20,
        "target_end_date_offset_days": 40,
        "priority": "critical",
        "health_status": "healthy",
        "delivery_notes": (
            "MVP focuses on catalog, work management, projects and organization management."
        ),
    },
    {
        "name": "Core Design System Foundation",
        "project_type": "internal_project",
        "status": "active",
        "owner_email": "sofia.marin@example.com",
        "team": "Core Platform Team",
        "capability": "Product Management",
        "start_date_offset_days": -10,
        "target_end_date_offset_days": 20,
        "priority": "medium",
        "health_status": "healthy",
        "delivery_notes": "Defines minimal enterprise UI patterns and reusable components.",
    },
    {
        "name": "Data Governance Operating Model",
        "project_type": "internal_project",
        "status": "planned",
        "owner_email": "emma.johnson@example.com",
        "team": "Governance Team",
        "capability": "Data Governance",
        "start_date_offset_days": 10,
        "target_end_date_offset_days": 80,
        "priority": "high",
        "health_status": "unknown",
        "delivery_notes": (
            "Will define compliance rules, policies, team checks and evidence model."
        ),
    },
]

DATA_PRODUCTS: list[DataProductSeed] = [
    {
        "name": "Executive Sales Dashboard",
        "description": (
            "Business-facing dashboard for leadership to monitor revenue, margin, "
            "sell-through and regional sales trends."
        ),
        "type": "dashboard",
        "status": "active",
        "quality_status": "good",
        "business_domain": "Sales",
        "business_owner_email": "lucas.ferreira@example.com",
        "technical_owner_email": "maya.singh@example.com",
        "capability": "BI",
        "team": "Data Products Team",
        "refresh_frequency": "Daily",
        "source_systems": "ERP, POS, E-commerce platform",
        "consumers": "CEO, CFO, Sales Leadership, Regional Managers",
        "documentation_url": "https://example.com/docs/executive-sales-dashboard",
    },
    {
        "name": "Inventory Health Dataset",
        "description": (
            "Curated dataset for stock availability, replenishment, warehouse health "
            "and aging inventory analysis."
        ),
        "type": "dataset",
        "status": "active",
        "quality_status": "warning",
        "business_domain": "Inventory",
        "business_owner_email": "maya.singh@example.com",
        "technical_owner_email": "tom.becker@example.com",
        "capability": "Data Engineering",
        "team": "Data Products Team",
        "refresh_frequency": "Every 4 hours",
        "source_systems": "ERP, WMS, Replenishment system",
        "consumers": "Supply Chain, Merchandising, BI Team",
        "documentation_url": "https://example.com/docs/inventory-health-dataset",
    },
    {
        "name": "Finance KPI Layer",
        "description": (
            "Certified KPI layer for finance reporting, including revenue, margin, cost, "
            "budget and forecast metrics."
        ),
        "type": "metric",
        "status": "active",
        "quality_status": "good",
        "business_domain": "Finance",
        "business_owner_email": "emma.johnson@example.com",
        "technical_owner_email": "daniel.weber@example.com",
        "capability": "Data Governance",
        "team": "Governance Team",
        "refresh_frequency": "Daily",
        "source_systems": "ERP, Planning system, Consolidation system",
        "consumers": "Finance, CFO Office, BI Team",
        "documentation_url": "https://example.com/docs/finance-kpi-layer",
    },
    {
        "name": "AI Report Generator",
        "description": (
            "AI-assisted report generation product that creates first draft management "
            "summaries from approved data products."
        ),
        "type": "ai_agent",
        "status": "draft",
        "quality_status": "unknown",
        "business_domain": "Operations",
        "business_owner_email": "sofia.marin@example.com",
        "technical_owner_email": "omar.haddad@example.com",
        "capability": "AI",
        "team": "AI Enablement Team",
        "refresh_frequency": "On demand",
        "source_systems": "Approved data products, KPI catalog, report templates",
        "consumers": "Product Owners, BI Team, Leadership",
        "documentation_url": "https://example.com/docs/ai-report-generator",
    },
    {
        "name": "Product Master Data Product",
        "description": (
            "Governed product master data product with product attributes, hierarchy, "
            "style, color and lifecycle status."
        ),
        "type": "dataset",
        "status": "active",
        "quality_status": "warning",
        "business_domain": "Product",
        "business_owner_email": "daniel.weber@example.com",
        "technical_owner_email": "maya.singh@example.com",
        "capability": "Data Engineering",
        "team": "Data Products Team",
        "refresh_frequency": "Daily",
        "source_systems": "PLM, ERP, PIM",
        "consumers": "Merchandising, E-commerce, BI, AI Search",
        "documentation_url": "https://example.com/docs/product-master-data",
    },
    {
        "name": "Regional Sales Mart",
        "description": "Regional sales mart for territory managers — ownership assignment pending.",
        "type": "dataset",
        "status": "active",
        "quality_status": "good",
        "business_domain": "Sales",
        "technical_owner_email": "maya.singh@example.com",
        "capability": "BI",
        "team": "Data Products Team",
        "refresh_frequency": "Daily",
        "source_systems": "ERP, CRM",
        "consumers": "Regional Managers",
        "documentation_url": None,
    },
    {
        "name": "Project Delivery Health Report",
        "description": (
            "Report for tracking delivery health, open risks, delayed work items "
            "and project capacity indicators."
        ),
        "type": "report",
        "status": "draft",
        "quality_status": "unknown",
        "business_domain": "Operations",
        "business_owner_email": "grace.lee@example.com",
        "technical_owner_email": "lucas.ferreira@example.com",
        "capability": "BI",
        "team": "Delivery Operations Team",
        "refresh_frequency": "Weekly",
        "source_systems": "Internal Sea",
        "consumers": "Leadership, Project Managers, Capability Leads",
        "documentation_url": "https://example.com/docs/project-delivery-health-report",
    },
]

WORK_ITEMS: list[WorkItemSeed] = [
    {
        "title": "Create Data Product Catalog API",
        "type": "task",
        "status": "done",
        "priority": "high",
        "assignee_email": "maya.singh@example.com",
        "reporter_email": "nikita@example.com",
        "project": "Internal Sea MVP",
        "data_product": "Product Master Data Product",
        "capability": "Data Engineering",
        "team": "Core Platform Team",
        "due_date_offset_days": -5,
        "estimate_points": 5,
    },
    {
        "title": "Build Data Product Catalog UI",
        "type": "task",
        "status": "done",
        "priority": "high",
        "assignee_email": "sofia.marin@example.com",
        "reporter_email": "nikita@example.com",
        "project": "Internal Sea MVP",
        "capability": "Product Management",
        "team": "Core Platform Team",
        "due_date_offset_days": -2,
        "estimate_points": 8,
    },
    {
        "title": "Add Work Board",
        "type": "improvement",
        "status": "review",
        "priority": "medium",
        "assignee_email": "grace.lee@example.com",
        "reporter_email": "sofia.marin@example.com",
        "project": "Internal Sea MVP",
        "capability": "Business Analysis",
        "team": "Delivery Operations Team",
        "due_date_offset_days": 3,
        "estimate_points": 5,
    },
    {
        "title": "Define relationship layer model",
        "type": "technical_debt",
        "status": "backlog",
        "priority": "high",
        "assignee_email": "daniel.weber@example.com",
        "reporter_email": "nikita@example.com",
        "project": "Internal Sea MVP",
        "capability": "Architecture",
        "team": "Core Platform Team",
        "due_date_offset_days": 14,
        "estimate_points": 8,
    },
    {
        "title": "Missing auth and permissions",
        "type": "risk",
        "status": "ready",
        "priority": "critical",
        "assignee_email": "anna.kowalski@example.com",
        "reporter_email": "nikita@example.com",
        "project": "Internal Sea MVP",
        "capability": "CloudOps",
        "team": "Core Platform Team",
        "due_date_offset_days": 10,
        "estimate_points": 8,
    },
    {
        "title": "Overdue: Complete sales mart ownership assignment",
        "type": "task",
        "status": "in_progress",
        "priority": "critical",
        "assignee_email": "lucas.ferreira@example.com",
        "reporter_email": "nikita@example.com",
        "project": "Internal Sea MVP",
        "data_product": "Regional Sales Mart",
        "capability": "Data Governance",
        "team": "Data Products Team",
        "due_date_offset_days": -4,
        "estimate_points": 3,
    },
    {
        "title": "Validate Finance KPI definitions",
        "type": "task",
        "status": "in_progress",
        "priority": "high",
        "assignee_email": "emma.johnson@example.com",
        "reporter_email": "nikita@example.com",
        "project": "Finance Data Platform Migration",
        "data_product": "Finance KPI Layer",
        "capability": "Data Governance",
        "team": "Governance Team",
        "due_date_offset_days": 7,
        "estimate_points": 5,
    },
    {
        "title": "Reconcile inventory source systems",
        "type": "bug",
        "status": "ready",
        "priority": "high",
        "assignee_email": "maya.singh@example.com",
        "reporter_email": "daniel.weber@example.com",
        "project": "Finance Data Platform Migration",
        "data_product": "Inventory Health Dataset",
        "capability": "Data Engineering",
        "team": "Data Products Team",
        "due_date_offset_days": 5,
        "estimate_points": 8,
    },
    {
        "title": "Confirm dashboard consumers",
        "type": "story",
        "status": "in_progress",
        "priority": "medium",
        "assignee_email": "grace.lee@example.com",
        "reporter_email": "lucas.ferreira@example.com",
        "project": "Executive Reporting Foundation",
        "data_product": "Executive Sales Dashboard",
        "capability": "Business Analysis",
        "team": "Delivery Operations Team",
        "due_date_offset_days": 4,
        "estimate_points": 3,
    },
    {
        "title": "Decide ownership model for Finance KPI Layer",
        "type": "decision",
        "status": "review",
        "priority": "medium",
        "assignee_email": "emma.johnson@example.com",
        "reporter_email": "nikita@example.com",
        "project": "Finance Data Platform Migration",
        "data_product": "Finance KPI Layer",
        "capability": "Data Governance",
        "team": "Governance Team",
        "due_date_offset_days": 2,
        "estimate_points": 2,
    },
    {
        "title": "Prepare AI governance pilot scope",
        "type": "epic",
        "status": "backlog",
        "priority": "high",
        "assignee_email": "omar.haddad@example.com",
        "reporter_email": "emma.johnson@example.com",
        "project": "AI Governance Pilot",
        "data_product": "AI Report Generator",
        "capability": "AI",
        "team": "AI Enablement Team",
        "due_date_offset_days": 20,
        "estimate_points": 13,
    },
]

RELATIONSHIPS: list[RelationshipSeed] = [
    {
        "source_type": "data_product",
        "source_key": "Executive Sales Dashboard",
        "target_type": "data_product",
        "target_key": "Finance KPI Layer",
        "link_type": "depends_on",
        "title": "Dashboard depends on KPI layer",
    },
    {
        "source_type": "data_product",
        "source_key": "AI Report Generator",
        "target_type": "data_product",
        "target_key": "Finance KPI Layer",
        "link_type": "depends_on",
        "title": "AI report depends on KPI definitions",
    },
    {
        "source_type": "data_product",
        "source_key": "Inventory Health Dataset",
        "target_type": "project",
        "target_key": "Finance Data Platform Migration",
        "link_type": "supports",
        "title": "Dataset supports migration project",
    },
    {
        "source_type": "work_item",
        "source_key": "Missing auth and permissions",
        "target_type": "internal_project",
        "target_key": "Internal Sea MVP",
        "link_type": "blocks",
        "title": "Auth work blocks MVP delivery",
    },
    {
        "source_type": "team",
        "source_key": "Core Platform Team",
        "target_type": "internal_project",
        "target_key": "Internal Sea MVP",
        "link_type": "owns",
        "title": "Core platform team owns MVP",
    },
    {
        "source_type": "capability",
        "source_key": "Data Governance",
        "target_type": "project",
        "target_key": "AI Governance Pilot",
        "link_type": "supports",
        "title": "Governance capability supports pilot",
    },
]

FILE_STORAGES: list[FileStorageSeed] = [
    {
        "name": "External Documentation",
        "storage_type": "external_url",
        "base_url": "https://example.com/docs",
        "description": "Demo external documentation links.",
        "is_active": True,
    },
    {
        "name": "SharePoint Demo",
        "storage_type": "sharepoint",
        "base_url": "https://example.com/sharepoint",
        "description": "Placeholder for future SharePoint integration.",
        "is_active": True,
    },
]

FILE_ASSETS: list[FileAssetSeed] = [
    {
        "name": "Executive Sales Dashboard Specification",
        "file_type": "specification",
        "status": "active",
        "sensitivity": "internal",
        "external_url": "https://example.com/docs/executive-sales-dashboard-spec",
        "version": "v1.0",
        "storage": "External Documentation",
        "entity_type": "data_product",
        "entity_key": "Executive Sales Dashboard",
        "purpose": "Functional specification",
        "is_evidence": True,
        "evidence_type": "business_approval",
    },
    {
        "name": "Finance KPI Definitions",
        "file_type": "evidence",
        "status": "active",
        "sensitivity": "confidential",
        "external_url": "https://example.com/docs/finance-kpi-definitions",
        "version": "v1.2",
        "storage": "External Documentation",
        "entity_type": "data_product",
        "entity_key": "Finance KPI Layer",
        "purpose": "Certified KPI definitions",
        "is_evidence": True,
        "evidence_type": "kpi_certification",
    },
    {
        "name": "Internal Sea MVP Scope",
        "file_type": "document",
        "status": "active",
        "sensitivity": "internal",
        "external_url": "https://example.com/docs/internal-sea-core-mvp-scope",
        "version": "v0.3",
        "storage": "External Documentation",
        "entity_type": "internal_project",
        "entity_key": "Internal Sea MVP",
        "purpose": "MVP scope document",
        "is_evidence": False,
    },
    {
        "name": "AI Governance Pilot Notes",
        "file_type": "document",
        "status": "draft",
        "sensitivity": "confidential",
        "external_url": "https://example.com/docs/ai-governance-pilot-notes",
        "version": "v0.1",
        "storage": "External Documentation",
        "entity_type": "project",
        "entity_key": "AI Governance Pilot",
        "purpose": "Pilot discovery notes",
        "is_evidence": True,
        "evidence_type": "discovery_evidence",
    },
]

COMPLIANCE_POLICIES: list[CompliancePolicySeed] = [
    {
        "name": "Data Product Governance Policy",
        "description": (
            "Defines minimum ownership, documentation, quality and evidence "
            "requirements for active data products."
        ),
        "status": "active",
        "owner_email": "emma.johnson@example.com",
        "version": "v1.0",
    },
    {
        "name": "Project Delivery Compliance Policy",
        "description": (
            "Defines required delivery controls for active client and internal projects."
        ),
        "status": "active",
        "owner_email": "grace.lee@example.com",
        "version": "v1.0",
    },
]

COMPLIANCE_RULES: list[ComplianceRuleSeed] = [
    {
        "policy": "Data Product Governance Policy",
        "code": "DPG-001",
        "name": "Active data products must have business owner",
        "severity": "high",
        "subject_type": "data_product",
    },
    {
        "policy": "Data Product Governance Policy",
        "code": "DPG-002",
        "name": "Active data products must have technical owner",
        "severity": "high",
        "subject_type": "data_product",
    },
    {
        "policy": "Data Product Governance Policy",
        "code": "DPG-003",
        "name": "Critical data products must have evidence of KPI or requirement approval",
        "severity": "medium",
        "subject_type": "data_product",
    },
    {
        "policy": "Project Delivery Compliance Policy",
        "code": "PDC-001",
        "name": "Active projects must have owner and team",
        "severity": "high",
        "subject_type": "project",
    },
    {
        "policy": "Project Delivery Compliance Policy",
        "code": "PDC-002",
        "name": "Projects with warning or critical health must have mitigation notes",
        "severity": "medium",
        "subject_type": "project",
    },
]

COMPLIANCE_CONTROLS: list[ComplianceControlSeed] = [
    {
        "rule_code": "DPG-001",
        "name": "Ownership Review Control",
        "description": "Verify business and technical owners are assigned.",
        "control_type": "manual",
        "status": "active",
        "frequency": "quarterly",
    },
    {
        "rule_code": "DPG-003",
        "name": "Documentation Evidence Control",
        "description": "Collect approved specification or KPI evidence.",
        "control_type": "detective",
        "status": "active",
        "frequency": "on_change",
    },
    {
        "rule_code": "PDC-002",
        "name": "Project Health Review Control",
        "description": "Review delivery health and mitigation notes.",
        "control_type": "manual",
        "status": "active",
        "frequency": "monthly",
    },
]

COMPLIANCE_CHECKS: list[ComplianceCheckSeed] = [
    {
        "title": "Business and technical ownership confirmed",
        "description": "Verify Executive Sales Dashboard has assigned owners.",
        "subject_type": "data_product",
        "subject_key": "Executive Sales Dashboard",
        "rule_code": "DPG-001",
        "control_name": "Ownership Review Control",
        "status": "compliant",
        "check_type": "manual",
        "result_summary": "Owners confirmed in catalog.",
        "evidence_file": "Executive Sales Dashboard Specification",
    },
    {
        "title": "Finance KPI definitions are certified",
        "description": "Certified KPI definitions attached as evidence.",
        "subject_type": "data_product",
        "subject_key": "Finance KPI Layer",
        "rule_code": "DPG-003",
        "control_name": "Documentation Evidence Control",
        "status": "compliant",
        "check_type": "review",
        "result_summary": "KPI definitions certified.",
        "evidence_file": "Finance KPI Definitions",
    },
    {
        "title": "MVP scope and delivery health reviewed",
        "description": "Internal Sea MVP scope document and health review.",
        "subject_type": "internal_project",
        "subject_key": "Internal Sea MVP",
        "rule_code": "PDC-002",
        "control_name": "Project Health Review Control",
        "status": "in_progress",
        "check_type": "manual",
        "result_summary": "Scope documented; health review ongoing.",
        "evidence_file": "Internal Sea MVP Scope",
    },
    {
        "title": "Inventory data quality review due",
        "description": "Quarterly inventory data quality review for warning-quality dataset.",
        "subject_type": "data_product",
        "subject_key": "Inventory Health Dataset",
        "rule_code": "DPG-002",
        "control_name": "Quality Review Control",
        "status": "in_progress",
        "check_type": "review",
        "due_date_offset_days": -3,
        "result_summary": "Review overdue — awaiting owner sign-off.",
    },
    {
        "title": "Discovery evidence collected",
        "description": "AI Governance Pilot discovery notes and evidence.",
        "subject_type": "project",
        "subject_key": "AI Governance Pilot",
        "rule_code": "PDC-001",
        "control_name": "Ownership Review Control",
        "status": "in_progress",
        "check_type": "self_assessment",
        "result_summary": "Discovery notes collected; ownership review pending.",
        "evidence_file": "AI Governance Pilot Notes",
    },
]


class AutomationScheduleSeed(TypedDict, total=False):
    name: str
    description: str
    frequency: str
    timezone: str
    is_active: bool


class AutomationTriggerSeed(TypedDict, total=False):
    name: str
    description: str
    status: str
    trigger_type: str
    action_type: str
    schedule: str
    target_type: str
    target_key: str
    action_config: dict[str, Any]
    next_run_at_past_minutes: int


AUTOMATION_SCHEDULES: list[AutomationScheduleSeed] = [
    {
        "name": "Monthly Data Product Review",
        "description": "Monthly review cadence for data product ownership and quality.",
        "frequency": "monthly",
        "timezone": "UTC",
        "is_active": True,
    },
    {
        "name": "Weekly Project Health Review",
        "description": "Weekly project health and delivery review cadence.",
        "frequency": "weekly",
        "timezone": "UTC",
        "is_active": True,
    },
    {
        "name": "Quarterly Compliance Evidence Review",
        "description": "Quarterly evidence and certification review cadence.",
        "frequency": "quarterly",
        "timezone": "UTC",
        "is_active": True,
    },
]

AUTOMATION_TRIGGERS: list[AutomationTriggerSeed] = [
    {
        "name": "Review Executive Sales Dashboard",
        "description": "Monthly reminder to review dashboard documentation and quality.",
        "status": "active",
        "trigger_type": "schedule",
        "action_type": "create_work_item",
        "schedule": "Monthly Data Product Review",
        "target_type": "data_product",
        "target_key": "Executive Sales Dashboard",
        "next_run_at_past_minutes": 5,
        "action_config": {
            "title": "Review Executive Sales Dashboard documentation",
            "description": (
                "Monthly review of ownership, documentation, refresh frequency "
                "and quality status."
            ),
            "priority": "medium",
            "type": "task",
            "due_in_days": 7,
        },
    },
    {
        "name": "Review Internal Sea MVP health",
        "description": "Weekly project health review automation.",
        "status": "active",
        "trigger_type": "schedule",
        "action_type": "create_activity_event",
        "schedule": "Weekly Project Health Review",
        "target_type": "internal_project",
        "target_key": "Internal Sea MVP",
        "action_config": {
            "title": "Weekly project health review",
            "description": "Review open work, risks, overdue items and project health.",
        },
    },
    {
        "name": "Check Finance KPI evidence",
        "description": "Quarterly reminder to review KPI certification evidence.",
        "status": "active",
        "trigger_type": "schedule",
        "action_type": "add_comment",
        "schedule": "Quarterly Compliance Evidence Review",
        "target_type": "data_product",
        "target_key": "Finance KPI Layer",
        "action_config": {
            "body": "Quarterly reminder to review KPI certification evidence.",
        },
    },
]


class PerformanceMetricDefinitionSeed(TypedDict, total=False):
    code: str
    name: str
    description: str
    subject_type: str
    value_type: str
    direction: str
    frequency: str
    status: str
    unit: str
    target_value: str
    warning_threshold: str
    critical_threshold: str
    owner_email: str | None


class PerformanceMetricValueSeed(TypedDict, total=False):
    metric_code: str
    subject_type: str
    subject_key: str
    value_numeric: str
    frequency: str
    source: str


PERFORMANCE_METRIC_DEFINITIONS: list[PerformanceMetricDefinitionSeed] = [
    {
        "code": "DP_QUALITY_SCORE",
        "name": "Data Product Quality Score",
        "description": "Composite quality score for data products.",
        "subject_type": "data_product",
        "value_type": "score",
        "direction": "higher_is_better",
        "frequency": "monthly",
        "status": "active",
        "unit": "points",
        "target_value": "90",
        "warning_threshold": "75",
        "critical_threshold": "60",
        "owner_email": "emma.johnson@example.com",
    },
    {
        "code": "DOC_COVERAGE",
        "name": "Documentation Coverage",
        "description": "Percentage of required documentation completed.",
        "subject_type": "data_product",
        "value_type": "percentage",
        "direction": "higher_is_better",
        "frequency": "monthly",
        "status": "active",
        "unit": "%",
        "target_value": "95",
        "warning_threshold": "80",
        "critical_threshold": "60",
    },
    {
        "code": "OPEN_WORK_ITEMS",
        "name": "Open Work Items",
        "description": "Count of open work items on a project.",
        "subject_type": "project",
        "value_type": "count",
        "direction": "lower_is_better",
        "frequency": "weekly",
        "status": "active",
        "unit": "items",
        "target_value": "10",
        "warning_threshold": "20",
        "critical_threshold": "30",
    },
    {
        "code": "PROJECT_HEALTH_SCORE",
        "name": "Project Delivery Health Score",
        "description": "Composite delivery health score for projects.",
        "subject_type": "project",
        "value_type": "score",
        "direction": "higher_is_better",
        "frequency": "weekly",
        "status": "active",
        "unit": "points",
        "target_value": "85",
        "warning_threshold": "70",
        "critical_threshold": "50",
    },
    {
        "code": "TEAM_UTILIZATION",
        "name": "Team Utilization",
        "description": "Team utilization percentage.",
        "subject_type": "team",
        "value_type": "percentage",
        "direction": "target_is_best",
        "frequency": "monthly",
        "status": "active",
        "unit": "%",
        "target_value": "80",
        "warning_threshold": "60",
        "critical_threshold": "40",
    },
    {
        "code": "CAPABILITY_WORKLOAD",
        "name": "Capability Workload",
        "description": "Open items assigned to a capability.",
        "subject_type": "capability",
        "value_type": "count",
        "direction": "lower_is_better",
        "frequency": "weekly",
        "status": "active",
        "unit": "open items",
        "target_value": "15",
        "warning_threshold": "25",
        "critical_threshold": "35",
    },
    {
        "code": "PERSON_AVAILABILITY",
        "name": "Person Availability",
        "description": "Person availability percentage.",
        "subject_type": "person",
        "value_type": "percentage",
        "direction": "target_is_best",
        "frequency": "monthly",
        "status": "active",
        "unit": "%",
        "target_value": "80",
    },
]

PERFORMANCE_METRIC_VALUES: list[PerformanceMetricValueSeed] = [
    {
        "metric_code": "DP_QUALITY_SCORE",
        "subject_type": "data_product",
        "subject_key": "Executive Sales Dashboard",
        "value_numeric": "92",
        "frequency": "monthly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "DOC_COVERAGE",
        "subject_type": "data_product",
        "subject_key": "Executive Sales Dashboard",
        "value_numeric": "88",
        "frequency": "monthly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "DP_QUALITY_SCORE",
        "subject_type": "data_product",
        "subject_key": "Inventory Health Dataset",
        "value_numeric": "74",
        "frequency": "monthly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "DOC_COVERAGE",
        "subject_type": "data_product",
        "subject_key": "Inventory Health Dataset",
        "value_numeric": "67",
        "frequency": "monthly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "OPEN_WORK_ITEMS",
        "subject_type": "project",
        "subject_key": "Finance Data Platform Migration",
        "value_numeric": "14",
        "frequency": "weekly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "PROJECT_HEALTH_SCORE",
        "subject_type": "project",
        "subject_key": "Finance Data Platform Migration",
        "value_numeric": "72",
        "frequency": "weekly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "OPEN_WORK_ITEMS",
        "subject_type": "internal_project",
        "subject_key": "Internal Sea MVP",
        "value_numeric": "8",
        "frequency": "weekly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "PROJECT_HEALTH_SCORE",
        "subject_type": "internal_project",
        "subject_key": "Internal Sea MVP",
        "value_numeric": "86",
        "frequency": "weekly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "TEAM_UTILIZATION",
        "subject_type": "team",
        "subject_key": "Data Products Team",
        "value_numeric": "82",
        "frequency": "monthly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "TEAM_UTILIZATION",
        "subject_type": "team",
        "subject_key": "Core Platform Team",
        "value_numeric": "76",
        "frequency": "monthly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "CAPABILITY_WORKLOAD",
        "subject_type": "capability",
        "subject_key": "Data Engineering",
        "value_numeric": "18",
        "frequency": "weekly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "CAPABILITY_WORKLOAD",
        "subject_type": "capability",
        "subject_key": "Data Governance",
        "value_numeric": "9",
        "frequency": "weekly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "PERSON_AVAILABILITY",
        "subject_type": "person",
        "subject_key": "nikita@example.com",
        "value_numeric": "70",
        "frequency": "monthly",
        "source": "Manual demo seed",
    },
    {
        "metric_code": "PERSON_AVAILABILITY",
        "subject_type": "person",
        "subject_key": "maya.singh@example.com",
        "value_numeric": "90",
        "frequency": "monthly",
        "source": "Manual demo seed",
    },
]


class AuthUserSeed(TypedDict):
    email: str
    password: str
    full_name: str
    role: str
    is_superuser: bool
    is_active: bool


# Local demo credentials only — do not use in production.
DEMO_AUTH_USERS: list[AuthUserSeed] = [
    {
        "email": "admin@example.com",
        "password": "admin12345",
        "full_name": "Admin User",
        "role": "admin",
        "is_superuser": True,
        "is_active": True,
    },
    {
        "email": "editor@example.com",
        "password": "editor12345",
        "full_name": "Editor User",
        "role": "editor",
        "is_superuser": False,
        "is_active": True,
    },
    {
        "email": "viewer@example.com",
        "password": "viewer12345",
        "full_name": "Viewer User",
        "role": "viewer",
        "is_superuser": False,
        "is_active": True,
    },
]


class NotificationChannelSeed(TypedDict, total=False):
    name: str
    channel_type: str
    status: str
    description: str
    endpoint_url: str
    default_recipient: str
    provider_config: dict[str, Any]


class NotificationTemplateSeed(TypedDict, total=False):
    name: str
    status: str
    event_type: str
    subject_template: str
    body_template: str
    description: str


class NotificationMessageSeed(TypedDict, total=False):
    channel: str
    template: str | None
    status: str
    priority: str
    event_type: str
    subject: str
    body: str
    recipient_type: str
    recipient_value: str
    entity_type: str
    entity_key: str
    simulated: bool
    scheduled_at_past_minutes: int
    error_message: str


class NotificationPreferenceSeed(TypedDict):
    user_email: str
    channel_type: str
    event_type: str
    is_enabled: bool


NOTIFICATION_CHANNELS: list[NotificationChannelSeed] = [
    {
        "name": "Local In-App Notifications",
        "channel_type": "in_app",
        "status": "active",
        "description": "Local MVP notification records without external delivery.",
        "default_recipient": "admin@example.com",
    },
    {
        "name": "Demo Email Channel",
        "channel_type": "email",
        "status": "draft",
        "description": "Placeholder for future email provider integration.",
        "default_recipient": "team@example.com",
    },
    {
        "name": "Demo Teams Channel",
        "channel_type": "teams",
        "status": "draft",
        "description": "Placeholder for future Microsoft Teams webhook integration.",
    },
]

NOTIFICATION_TEMPLATES: list[NotificationTemplateSeed] = [
    {
        "name": "Data Product Review Reminder",
        "status": "active",
        "event_type": "data_product_review",
        "subject_template": "Data product review: {{title}}",
        "body_template": "Please review {{title}}. Entity: {{entity_type}}/{{entity_id}}.",
    },
    {
        "name": "Compliance Due Reminder",
        "status": "active",
        "event_type": "compliance_due",
        "subject_template": "Compliance check due: {{title}}",
        "body_template": "Compliance check {{title}} requires review. Status: {{status}}.",
    },
    {
        "name": "Automation Run Notification",
        "status": "active",
        "event_type": "automation_run",
        "subject_template": "Automation run: {{title}}",
        "body_template": (
            "Automation event for {{entity_type}}/{{entity_id}} "
            "finished with status {{status}}."
        ),
    },
]

NOTIFICATION_MESSAGES: list[NotificationMessageSeed] = [
    {
        "channel": "Local In-App Notifications",
        "template": "Data Product Review Reminder",
        "status": "simulated",
        "priority": "normal",
        "event_type": "data_product_review",
        "subject": "Data product review: Executive Sales Dashboard",
        "body": "Please review Executive Sales Dashboard. Entity: data_product/demo.",
        "recipient_type": "email",
        "recipient_value": "admin@example.com",
        "entity_type": "data_product",
        "entity_key": "Executive Sales Dashboard",
        "simulated": True,
    },
    {
        "channel": "Local In-App Notifications",
        "template": "Compliance Due Reminder",
        "status": "draft",
        "priority": "high",
        "event_type": "compliance_due",
        "subject": "Compliance check due: Finance KPI definitions are certified",
        "body": "Compliance check Finance KPI definitions are certified requires review.",
        "recipient_type": "email",
        "recipient_value": "governance@example.com",
        "entity_type": "compliance_check",
        "entity_key": "Finance KPI definitions are certified",
        "simulated": False,
    },
    {
        "channel": "Local In-App Notifications",
        "status": "queued",
        "priority": "normal",
        "event_type": "manual",
        "subject": "Demo queued notification",
        "body": "This message is ready for worker processing.",
        "recipient_type": "email",
        "recipient_value": "admin@example.com",
        "scheduled_at_past_minutes": 5,
        "simulated": False,
    },
    {
        "channel": "Local In-App Notifications",
        "status": "failed",
        "priority": "high",
        "event_type": "work_item_due",
        "subject": "Demo failed delivery: overdue work reminder",
        "body": "Reminder for overdue critical work item could not be delivered.",
        "recipient_type": "email",
        "recipient_value": "editor@example.com",
        "entity_type": "work_item",
        "entity_key": "Overdue: Complete sales mart ownership assignment",
        "error_message": "Simulated delivery failure for dashboard demo.",
        "simulated": False,
    },
]

NOTIFICATION_PREFERENCES: list[NotificationPreferenceSeed] = [
    {
        "user_email": "admin@example.com",
        "channel_type": "in_app",
        "event_type": "manual",
        "is_enabled": True,
    },
    {
        "user_email": "editor@example.com",
        "channel_type": "in_app",
        "event_type": "work_item_due",
        "is_enabled": True,
    },
    {
        "user_email": "viewer@example.com",
        "channel_type": "in_app",
        "event_type": "project_health",
        "is_enabled": True,
    },
]


# Aggregate export for tests and documentation.
SEED_DATASETS: dict[str, list[Any]] = {
    "capabilities": CAPABILITIES,
    "teams": TEAMS,
    "people": PEOPLE,
    "business_domains": BUSINESS_DOMAINS,
    "client_projects": CLIENT_PROJECTS,
    "internal_projects": INTERNAL_PROJECTS,
    "data_products": DATA_PRODUCTS,
    "work_items": WORK_ITEMS,
    "relationships": RELATIONSHIPS,
    "file_storages": FILE_STORAGES,
    "file_assets": FILE_ASSETS,
    "compliance_policies": COMPLIANCE_POLICIES,
    "compliance_rules": COMPLIANCE_RULES,
    "compliance_controls": COMPLIANCE_CONTROLS,
    "compliance_checks": COMPLIANCE_CHECKS,
    "automation_schedules": AUTOMATION_SCHEDULES,
    "automation_triggers": AUTOMATION_TRIGGERS,
    "notification_channels": NOTIFICATION_CHANNELS,
    "notification_templates": NOTIFICATION_TEMPLATES,
    "notification_messages": NOTIFICATION_MESSAGES,
    "notification_preferences": NOTIFICATION_PREFERENCES,
}
