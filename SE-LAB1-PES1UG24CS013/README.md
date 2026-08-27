# Patient Health Record Consent Management System

**PES University — Dept. of CSE**
**Lab 1: Requirements Engineering & UML Use-Case Modelling**
**Problem Statement #13 | Healthcare & Telemedicine**

## Problem Context

A patient-centric electronic health data gateway where patients explicitly manage granular, time-bound consent permissions for clinics, diagnostic labs, and consulting doctors to access their medical history.

**Actors:** Patient, Clinic Administrator

## Repository Contents

| File | Deliverable |
|---|---|
| [`Requirements_Table.docx`](./Requirements_Table.docx) | Complete requirements table — 5 Functional Requirements (FR-001–FR-005) and 2 Non-Functional Requirements (NFR-001, NFR-002), each with ID, Type (NFRs), Description, Priority, Acceptance Criteria, and Rationale |
| [`usecase_diagram.svg`](./usecase_diagram.svg) | UML Use-Case Diagram — all actors, primary use cases, with `«include»` and `«extend»` relationships |
| [`usecase_diagram.png`](./usecase_diagram.png) | PNG export of the use-case diagram, for quick preview on GitHub |
| [`UseCase_Flow_Specification.docx`](./UseCase_Flow_Specification.docx) | 1-page Use-Case Flow Specification for UC-01 "Grant Time-Bound Consent" (FR-001) — Preconditions, Postconditions, Main Success Scenario, and one Alternate Flow |

## Requirements Summary

### Functional Requirements

| ID | Description | Priority |
|---|---|---|
| FR-001 | Patients grant time-bounded (e.g., 24-hour) access permissions for specific diagnostic records to verified clinic doctors. | High |
| FR-002 | Patients revoke previously granted consent at any time, with immediate effect. | High |
| FR-003 | Clinic Administrator submits a scoped, time-bound consent access request for a named patient. | High |
| FR-004 | System verifies requesting clinic/doctor identity against a verified-provider registry before any request reaches the patient. | High |
| FR-005 | System notifies the patient in real time of new access requests and upcoming consent expiry. | Medium |

### Non-Functional Requirements

| ID | Type | Description | Priority |
|---|---|---|---|
| NFR-001 | Security & Auditability | All consent grant/revoke/access events are permanently written to an append-only, tamper-evident audit trail. | High |
| NFR-002 | Performance & Availability | Consent validity checks resolve within 300ms (P95); consent-verification service maintains 99.9% monthly uptime. | High |

## Use-Case Diagram Overview

- **Primary Actors:** Patient, Clinic Administrator
- **Secondary/System Actors:** Verified Provider Registry, Notification Service
- **Primary Use Cases:** Grant Time-Bound Consent (FR-001), Revoke Consent (FR-002), Request Patient Record Access (FR-003)
- **`«include»` relationships:**
  - *Grant Time-Bound Consent* includes *Verify Provider Identity* (FR-004)
  - *Request Patient Record Access* includes *Verify Provider Identity* (FR-004)
  - *Grant Time-Bound Consent*, *Revoke Consent*, and *Request Patient Record Access* each include *Record Audit Trail Entry* (NFR-001)
- **`«extend»` relationships:**
  - *Send Access-Request / Expiry Notification* (FR-005) extends *Grant Time-Bound Consent* — condition: `[expiry < 1 hr away]`
  - *Send Access-Request / Expiry Notification* (FR-005) extends *Request Patient Record Access* — condition: `[on new request]`

## Core Use Case: UC-01 — Grant Time-Bound Consent

See [`UseCase_Flow_Specification.docx`](./UseCase_Flow_Specification.docx) for the full specification, covering:
- Preconditions & Postconditions
- 10-step Main Success Scenario
- Alternate Flow A1: Provider Verification Fails

---
*Submitted as part of Lab 1 coursework — Requirements Engineering & UML Use-Case Modelling.*
# SE-Submissions-PES1UG24CS013
