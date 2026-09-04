# Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**PES University — Department of Computer Science and Engineering**  
**Course:** Software Engineering (UE24CS242B)  
**Problem Statement #13 | Healthcare & Telemedicine:** Patient Health Record Consent Management System  
**Student SRN:** PES1UG24CS013  
**Jira Cloud Instance:** [https://abhays11.atlassian.net](https://abhays11.atlassian.net)

---

## 1. Quick Links to Live Jira Project

| View | Direct Jira URL |
|---|---|
| **Active Scrum Board** | [PHR Board (Board #35)](https://abhays11.atlassian.net/jira/software/c/projects/PHR/boards/35) |
| **Product Backlog & Epics** | [PHR Backlog & Epics Panel](https://abhays11.atlassian.net/jira/software/c/projects/PHR/boards/35/backlog) |
| **Burndown Chart** | [PHR Sprint 1 Burndown Chart](https://abhays11.atlassian.net/jira/software/c/projects/PHR/boards/35/reports/burndown-chart?sprint=36) |
| **Sprint Retrospective Report** | [PHR Sprint 1 Sprint Report](https://abhays11.atlassian.net/jira/software/c/projects/PHR/boards/35/reports/sprint-retrospective?sprint=36) |

---

## 2. Executive Summary & Problem Context

In Lab 1, requirements were formulated for the **Patient Health Record Consent Management System**—a patient-centric electronic health data gateway where patients explicitly manage granular, time-bound consent permissions for clinics, diagnostic labs, and consulting doctors to access their medical history.

In this laboratory (Lab 2), these requirements are translated into Agile artifacts:
- **Epics** representing macro-level functional themes.
- **User Stories** written from the end-user perspective (`As a... I want to... So that...`).
- **Story Points** assigned via the **Fibonacci scale** using **Planning Poker** principles based on effort, complexity, and uncertainty.
- **Sprint Simulation** executing a 1-week time-boxed iteration (Sprint 1) moving work items across `To Do` → `In Progress` → `Done`.
- **Burndown Chart Analysis** and evaluation through structured Agile reflection questions.

---

## 3. Epics Breakdown

The system's functional and non-functional requirements from Lab 1 are partitioned into three core Epics in Jira:

| Jira Key | Epic Name | Scope & Requirements | Target Actors |
|---|---|---|---|
| **PHR-1** | **Epic 1: Patient Consent Administration & Granular Permissions** | Provide patients with autonomous, granular controls to grant, configure, and instantly revoke time-bounded consent for their electronic medical history (FR-001, FR-002). | Patient |
| **PHR-2** | **Epic 2: Healthcare Provider Scoped Access & Identity Verification** | Enable clinic administrators to request scoped access to diagnostic records while enforcing strict cryptographic and registry-based doctor/clinic verification at the system boundary (FR-003, FR-004). | Clinic Administrator, Verified Provider Registry |
| **PHR-3** | **Epic 3: Real-Time Alerts & Immutable Audit Trail** | Deliver immediate notification alerts to patients for new requests and approaching consent expirations, backed by an immutable, append-only audit trail meeting strict performance and security thresholds (FR-005, NFR-001, NFR-002). | Patient, Notification Service, System Auditor |

---

## 4. Product Backlog: User Stories & Story Point Estimation

### 4.1 Agile User Stories Specification

| Story ID | Jira Key | Parent Epic | User Story (`As a... I want to... So that...`) | Priority | Story Points | Planning Poker Rationale | Sprint Status |
|---|---|---|---|:---:|:---:|---|:---:|
| **US-01** | **PHR-4** | Epic 1 (`PHR-1`) | **As a** patient,<br>**I want to** grant time-bounded (e.g., 24-hour) access permissions for specific diagnostic records to verified clinic doctors,<br>**So that** my sensitive medical history is accessible only during my active consultation and auto-revoked thereafter. | **High** | **5** | Requires parameter validation, granular record selection, expiry timestamp computation, and timer scheduling. Moderate complexity. | **Done** (Sprint 1) |
| **US-02** | **PHR-5** | Epic 1 (`PHR-1`) | **As a** patient,<br>**I want to** revoke previously granted consent at any time before its natural expiry with immediate effect,<br>**So that** clinics or doctors are instantly blocked if my consultation terminates early or circumstances change. | **High** | **3** | Direct state-transition mutation and token invalidation. Low uncertainty, well-defined operational logic. | **Done** (Sprint 1) |
| **US-03** | **PHR-6** | Epic 2 (`PHR-2`) | **As a** clinic administrator,<br>**I want to** submit a scoped, time-bound consent access request for a named patient,<br>**So that** attending doctors can legally review relevant medical history for diagnostic procedures. | **High** | **5** | Involves complex multi-field form inputs, clinical taxonomy filtering, patient resolution, and state persistence. | **Done** (Sprint 1) |
| **US-04** | **PHR-7** | Epic 2 (`PHR-2`) | **As a** healthcare security gateway,<br>**I want to** verify requesting clinic and doctor identities against the verified-provider registry before forwarding requests to the patient,<br>**So that** impersonators, uncertified entities, or blacklisted practitioners are rejected at the perimeter. | **High** | **8** | High uncertainty and architectural complexity: involves synchronous third-party API integration, mTLS handshake, fallback caches, and strict error handling. | **Done** (Sprint 1) |
| **US-05** | **PHR-8** | Epic 3 (`PHR-3`) | **As a** patient,<br>**I want to** receive real-time notifications for incoming access requests and alerts 1 hour before active consent expires,<br>**So that** I stay informed and can act proactively to grant or extend permissions. | **Medium** | **3** | Event-driven webhook and mobile push notification delivery. Standard communication pattern with low architectural risk. | **Staged** (Sprint 2) |
| **US-06** | **PHR-9** | Epic 3 (`PHR-3`) | **As a** compliance officer,<br>**I want** all consent grant, revoke, and access events permanently written to an append-only, tamper-evident audit trail,<br>**So that** legal non-repudiation, DPDP/HIPAA regulatory compliance, and post-incident forensic audits are guaranteed. | **High** | **5** | Append-only write pipeline, cryptographic checksumming/hash-chaining, and P95 latency constraint (<300ms). | **Staged** (Sprint 2) |

---

### 4.2 Acceptance Criteria per User Story

* **US-01: Time-Bound Consent Grant (`PHR-4`)**  
  *Pass:* Doctor access automatically revokes upon expiry timestamp.  
  *Fail:* Doctor retains or gains access to records after consent expiration.
* **US-02: Immediate Consent Revocation (`PHR-5`)**  
  *Pass:* Access attempt made 1 second after manual revocation is denied (HTTP 403) and logged.  
  *Fail:* Clinic/doctor retains access after the patient has revoked consent.
* **US-03: Scoped Clinic Access Request Submission (`PHR-6`)**  
  *Pass:* Request specifies scope, required records, and duration, and is delivered to patient inbox.  
  *Fail:* Missing mandatory clinical metadata or patient identifier is accepted.
* **US-04: Provider Identity Verification Gateway (`PHR-7`)**  
  *Pass:* Verified doctor active in national registry allows request propagation.  
  *Fail:* Suspended or invalid doctor credentials allow request delivery without validation.
* **US-05: Real-Time Alerts & Reminders (`PHR-8`)**  
  *Pass:* Patient receives push notification within 2 seconds of request submission and 1 hour before expiry.  
  *Fail:* Notifications dropped or delivered after consent expiration.
* **US-06: Append-Only Immutable Audit Trail (`PHR-9`)**  
  *Pass:* All events logged with cryptographic digest under 300ms latency; records cannot be updated or deleted.  
  *Fail:* Any audit trail record can be updated, deleted, or truncated.

---

## 5. Sprint Simulation: Sprint 1 & Sprint 2

### 5.1 Sprint 1 Execution Summary
* **Sprint Name:** `PHR Sprint 1` (Jira Sprint ID: `36`)
* **Duration:** 1 Week (Simulated Iteration)
* **Sprint Goal:** Deliver end-to-end patient consent granting, immediate revocation, and provider identity validation gateway (FR-001 to FR-004).
* **Committed & Completed Scope:**
  - `PHR-4` (US-01): 5 Story Points → **Done**
  - `PHR-5` (US-02): 3 Story Points → **Done**
  - `PHR-6` (US-03): 5 Story Points → **Done**
  - `PHR-7` (US-04): 8 Story Points → **Done**
* **Total Velocity Achieved:** **21 Story Points** (100% completion rate).

### 5.2 Sprint 2 Setup
* **Sprint Name:** `PHR Sprint 2` (Jira Sprint ID: `37`)
* **Sprint Goal:** Implement real-time patient alerts and append-only audit trail logging (FR-005, NFR-001, NFR-002).
* **Backlog Items Staged:**
  - `PHR-8` (US-05): 3 Story Points
  - `PHR-9` (US-06): 5 Story Points
* **Total Staged Velocity:** **8 Story Points**.

---

## 6. Jira Burndown Chart Analysis

### 6.1 Burndown Metrics
* **Total Story Points Committed:** 21 SP
* **Total Story Points Completed:** 21 SP
* **Scope Creep / Injected Stories:** 0 SP
* **Sprint Completion Rate:** 100%

### 6.2 Chart Trajectory Interpretation
* **Guideline (Ideal Burndown):** Displays a linear progression from 21 story points on Day 1 down to 0 story points on Day 7 (reducing at a constant rate of 3.0 points/day).
* **Actual Remaining Value (Burndown Line):**
  - **Day 1–2:** Team established API contracts and registry mocks (remaining: 21 SP).
  - **Day 3:** Completed atomic revocation `PHR-5` (3 SP) → Remaining drops to 18 SP.
  - **Day 4:** Completed time-bound consent grant `PHR-4` (5 SP) → Remaining drops to 13 SP.
  - **Day 5:** Completed scoped access request `PHR-6` (5 SP) → Remaining drops to 8 SP.
  - **Day 6–7:** Completed complex provider verification gateway `PHR-7` (8 SP) after end-to-end integration tests → Remaining drops to 0 SP.
* **Analysis:** The actual burndown tracked the ideal guideline closely. Prioritizing lower-complexity stories first established early velocity before tackling the high-uncertainty 8-point external integration.

---

## 7. Answers to Reflection Questions

### Question 1: Did your estimations reflect the actual effort?
> **Answer:**  
> Yes, the story point estimations closely reflected the actual implementation effort. By applying Planning Poker and the non-linear Fibonacci scale (1, 2, 3, 5, 8), the team effectively distinguished low-uncertainty internal tasks from complex external integrations:
> - **US-02 (`PHR-5`, 3 SP)** involved well-understood database state updates and cache token invalidation, proving straightforward and completing rapidly.
> - **US-01 (`PHR-4`, 5 SP)** and **US-03 (`PHR-6`, 5 SP)** required moderate effort due to validation logic, timestamp math, and clinical taxonomy filtering.
> - **US-04 (`PHR-7`, 8 SP)** accurately reflected the highest uncertainty, requiring live external registry API handshakes, TLS verification, and robust failure fallback mechanisms.  
> Using relative story points rather than hours allowed the team to capture technical risk and architectural complexity accurately.

### Question 2: Was your backlog well-prioritized?
> **Answer:**  
> Yes, the backlog was prioritized using a risk-first, value-driven Agile approach aligned with the MoSCoW method:
> - **Highest Priority (Must Haves):** `PHR-4` through `PHR-7` formed the foundational security and authorization layer. Without consent granting and doctor verification, the system cannot function ethically or legally. Hence, these were prioritized at the top of the backlog and scheduled into Sprint 1.
> - **Medium Priority (Should Haves):** `PHR-8` (Real-time notifications) provides great user convenience but relies upon the underlying access request pipeline. Prioritizing it for Sprint 2 ensured the core transaction engine was verified before alert pipelines were attached.
> This prioritization prevented blocking dependencies and minimized architectural rework.

### Question 3: How did your simulated sprint align with your plan?
> **Answer:**  
> The simulated sprint aligned strongly with the initial sprint plan:
> - The sprint timebox of 1 week was strictly respected.
> - All 4 committed user stories (21 story points) moved systematically from `To Do` to `In Progress` and finally to `Done` upon satisfying their acceptance criteria.
> - No uncontrolled scope creep occurred because new enhancement ideas were directed to the Product Backlog rather than injected into the active sprint.
> - The sprint goal—establishing end-to-end patient consent creation, immediate revocation, and provider identity validation—was completely fulfilled.

### Question 4: What insights did the burndown chart give about your team’s capacity?
> **Answer:**  
> The burndown chart provided three critical empirical insights:
> 1. **Empirical Velocity:** The team demonstrated a sustainable velocity of **21 story points per 1-week sprint**. This provides a reliable baseline for capacity planning in subsequent sprints.
> 2. **Batching vs. Continuous Flow:** The burndown showed stepped reductions rather than a single sudden cliff at the end of the sprint. This indicates that stories were broken down into sufficiently small batches that could be developed, tested, and marked Done continuously.
> 3. **Handling Complex Items:** The 8-point story (`PHR-7`) occupied the latter half of the sprint. For future sprints, the team can consider splitting 8-point stories into smaller 3-point and 5-point stories (e.g., separating mock verification from live registry integration) to achieve an even smoother burndown curve.

---

## 8. Jira Automation Script

The Python script [`scripts/jira_automation.py`](./scripts/jira_automation.py) was executed to create and configure the entire project in Jira Cloud via REST API v3 and Agile API v1.0.

### Execution Command:
```bash
python3 scripts/jira_automation.py --token <ATLASSIAN_API_TOKEN> --email abhsach@gmail.com --domain abhays11.atlassian.net
```
