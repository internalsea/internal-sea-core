# Compliance Feature

Policies, rules, controls, compliance checks and evidence for governance monitoring.

## Routes

| Route | Page |
|-------|------|
| `/compliance` | Overview, policies and checks tables |
| `/compliance/policies/new` | Create policy |
| `/compliance/policies/:id` | Policy detail with rules |
| `/compliance/policies/:id/edit` | Edit policy |
| `/compliance/checks/new` | Create check (`?subject_type=&subject_id=` supported) |
| `/compliance/checks/:id` | Check detail with evidence |
| `/compliance/checks/:id/edit` | Edit check |

## ComplianceSection

Embedded on detail pages:

- Data product (`subjectType="data_product"`)
- Project (`subjectType="project"`)
- Internal project (`subjectType="internal_project"`)
- Team (`subjectType="team"`)
- Capability (`subjectType="capability"`)

## Known limitations

- No entity picker — subject and file IDs are pasted manually
- No automated rule execution or scheduled checks
- No approval workflows or policy versioning UI
- Rule and control management is basic (rules on policy detail; controls via API)
