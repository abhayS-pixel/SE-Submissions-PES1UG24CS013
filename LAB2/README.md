# Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**PES University — Department of Computer Science and Engineering**  
**Course:** Software Engineering (UE24CS242B)  
**Problem Statement #13 | Healthcare & Telemedicine:** Patient Health Record Consent Management System  
**Student Name:** Abhay S  
**Student SRN:** PES1UG24CS013  
**Jira Cloud Instance:** [https://abhays11.atlassian.net](https://abhays11.atlassian.net) (Project: `PHR`, Board ID: `35`)

---

## 1. Submission Deliverables

| Deliverable File | Description | Format |
|---|---|:---:|
| [**`JIRA_LAB_SUBMISSION.pdf`**](./JIRA_LAB_SUBMISSION.pdf) | **Consolidated Submission Document** (Cover Page, Backlog & Epics, Sprints Timeline, Sprint 1 & 2 Burndown Charts, and Reflection Q&A) | PDF (3 Pages) |
| [**`Sprint_Reflection.pdf`**](./Sprint_Reflection.pdf) | **Deliverable 2: Sprint Reflection** (In-depth analysis answering all 4 lab reflection questions) | PDF (1 Page) |
| [**`Screenshot_Evidence.pdf`**](./Screenshot_Evidence.pdf) | **Deliverable 3: Jira Screenshots Evidence** (Backlog, Sprints Timeline, Sprint 1 Burndown, Sprint 2 Burndown) | PDF (4 Pages) |

---

## 2. Live Jira Cloud Verification Links

* **Active Scrum Board:** [PHR Board (#35)](https://abhays11.atlassian.net/jira/software/c/projects/PHR/boards/35)
* **Backlog & Epics Panel:** [PHR Backlog](https://abhays11.atlassian.net/jira/software/c/projects/PHR/boards/35/backlog)
* **Sprint 1 Burndown Chart (21 pts):** [Sprint 1 Report](https://abhays11.atlassian.net/jira/software/c/projects/PHR/boards/35/reports/burndown-chart?sprint=36)
* **Sprint 2 Burndown Chart (8 pts):** [Sprint 2 Report](https://abhays11.atlassian.net/jira/software/c/projects/PHR/boards/35/reports/burndown-chart?sprint=37)

---

## 3. Epics & Backlog Breakdown

### Epics
* **`PHR-1`** — **Epic 1: Patient Consent Administration & Granular Permissions** *(FR-001, FR-002)*
* **`PHR-2`** — **Epic 2: Healthcare Provider Scoped Access & Identity Verification** *(FR-003, FR-004)*
* **`PHR-3`** — **Epic 3: Real-Time Alerts & Immutable Audit Trail** *(FR-005, NFR-001, NFR-002)*

### User Stories & Story Points (Fibonacci Scale)
```
Expected story points: 1.1=5, 1.2=3, 2.1=5, 2.2=8, 3.1=3, 3.2=5. (Total = 29 SP)
```

| Jira Key | Story ID | Parent Epic | Priority | Story Points | Sprint | Status | User Story Summary |
|---|---|---|:---:|:---:|:---:|:---:|---|
| **`PHR-4`** | US-01 | `PHR-1` | **High** | **5** | Sprint 1 | **Done** | **Grant Time-Bound Consent:** Grant time-bounded (e.g., 24-hour) access permissions for specific diagnostic records to verified clinic doctors. |
| **`PHR-5`** | US-02 | `PHR-1` | **High** | **3** | Sprint 1 | **Done** | **Real-Time Consent Revocation:** Revoke previously granted consent at any time before natural expiry with immediate effect. |
| **`PHR-6`** | US-03 | `PHR-2` | **High** | **5** | Sprint 1 | **Done** | **Scoped Record Access Request:** Clinic administrator submits scoped, time-bound consent access request for a named patient. |
| **`PHR-7`** | US-04 | `PHR-2` | **High** | **8** | Sprint 1 | **Done** | **Provider Identity Verification Gateway:** Security gateway verifies requesting clinic/doctor identities against verified-provider registry. |
| **`PHR-8`** | US-05 | `PHR-3` | **Medium** | **3** | Sprint 2 | **Done** | **Real-Time Alerts & Expiry Reminders:** Patient receives real-time notifications for incoming access requests and alerts 1h before expiry. |
| **`PHR-9`** | US-06 | `PHR-3` | **High** | **5** | Sprint 2 | **Done** | **Append-Only Immutable Audit Trail:** All consent grant, revoke, and access events permanently logged to append-only tamper-evident trail. |

---

## 4. Sprint Simulation & Burndown Analysis

* **Sprint 1 (`PHR Sprint 1`, ID: 36):**
  - **Committed Scope:** `PHR-4` (5 pts), `PHR-5` (3 pts), `PHR-6` (5 pts), `PHR-7` (8 pts) = **21 Story Points**.
  - **Execution:** Moved across `To Do` → `In Progress` → `Done`, closed at 100% completion.
* **Sprint 2 (`PHR Sprint 2`, ID: 37):**
  - **Committed Scope:** `PHR-8` (3 pts), `PHR-9` (5 pts) = **8 Story Points**.
  - **Execution:** Moved across `To Do` → `In Progress` → `Done`, closed at 100% completion.

---

## 5. Summary of Reflection Responses

1. **Did your estimations reflect the actual effort?**  
   Yes. Higher-point stories like US-04 (`PHR-7`, 8 pts) involved significant external registry API handshakes, TLS verification, and failure timeouts, while low-point stories like US-02 (`PHR-5`, 3 pts) were atomic state transitions.
2. **Was your backlog well-prioritized?**  
   Yes. Core security and authorization workflows (US-01 through US-04) occupied Sprint 1, while auxiliary notifications (US-05) and audit loggers (US-06) were placed in Sprint 2.
3. **How did your simulated sprint align with your plan?**  
   Both Sprint 1 (21 pts) and Sprint 2 (8 pts) completed all committed user stories without scope creep, fulfilling their respective sprint goals.
4. **What insights did the burndown chart give about your team's capacity?**  
   Velocity was established at 21 pts (Sprint 1) and 8 pts (Sprint 2). The stepped curve demonstrated that 8-point stories should be broken down into 3- and 5-point sub-stories for smoother burndown progress.
