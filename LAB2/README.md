# Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**PES University — Department of Computer Science and Engineering**  
**Course:** Software Engineering (UE24CS242B)  
**Problem Statement #13 | Healthcare & Telemedicine:** Patient Health Record Consent Management System  
**Student SRN:** PES1UG24CS013  
**Jira Cloud Instance:** [https://abhays11.atlassian.net](https://abhays11.atlassian.net)

---

## 1. Executive Summary & Problem Context

In Lab 1, requirements were formulated for the **Patient Health Record Consent Management System**—a patient-centric electronic health data gateway where patients explicitly manage granular, time-bound consent permissions for clinics, diagnostic labs, and consulting doctors to access their medical history.

In this laboratory (Lab 2), these requirements are translated into Agile artifacts:
- **Epics** representing macro-level functional themes.
- **User Stories** written from the end-user perspective (`As a... I want to... So that...`).
- **Story Points** assigned via the **Fibonacci scale** using **Planning Poker** principles based on effort, complexity, and uncertainty.
- **Sprint Simulation** executing a 1-week time-boxed iteration (Sprint 1) moving work items across `To Do` → `In Progress` → `Done`.
- **Burndown Chart Analysis** and evaluation through structured Agile reflection questions.

---

## 2. Epics Breakdown

The system's functional and non-functional requirements from Lab 1 are partitioned into three core Epics:

### Epic 1: Patient Consent Administration & Granular Permissions
* **Summary:** Provide patients with autonomous, granular controls to grant, configure, and instantly revoke time-bounded consent for their electronic medical history.
* **Problem Scope:** Addresses FR-001 (Time-Bound Consent Grant) and FR-002 (Real-Time Consent Revocation).
* **Target Actors:** Patient.

### Epic 2: Healthcare Provider Scoped Access & Identity Verification
* **Summary:** Enable clinic administrators to request scoped access to diagnostic records while enforcing strict cryptographic and registry-based doctor/clinic verification at the system boundary.
* **Problem Scope:** Addresses FR-003 (Clinic Scoped Access Request) and FR-004 (Provider Identity Verification Gateway).
* **Target Actors:** Clinic Administrator, Verified Provider Registry (External Service).

### Epic 3: Real-Time Alerts & Immutable Audit Trail
* **Summary:** Deliver immediate notification alerts to patients for new requests and approaching consent expirations, backed by an immutable, append-only audit trail meeting strict performance and security thresholds.
* **Problem Scope:** Addresses FR-005 (Real-Time Patient Alerts), NFR-001 (Security & Auditability), and NFR-002 (Performance & Latency Standards).
* **Target Actors:** Patient, Notification Service, System Auditor.

---

## 3. Product Backlog: User Stories & Story Point Estimation

### 3.1 Agile User Stories Specification

| Story ID | Epic | User Story (`As a... I want to... So that...`) | Priority | Story Points | Planning Poker Rationale |
|---|---|---|:---:|:---:|---|
| **US-01** | Epic 1 | **As a** patient,<br>**I want to** grant time-bounded (e.g., 24-hour) access permissions for specific diagnostic records to verified clinic doctors,<br>**So that** my sensitive medical history is accessible only during my active consultation and auto-revoked thereafter. | **High** | **5** | Requires parameter validation, granular record selection, expiry timestamp computation, and timer scheduling. Moderate complexity. |
| **US-02** | Epic 1 | **As a** patient,<br>**I want to** revoke previously granted consent at any time before its natural expiry with immediate effect,<br>**So that** clinics or doctors are instantly blocked if my consultation terminates early or circumstances change. | **High** | **3** | Direct state-transition mutation and token invalidation. Low uncertainty, well-defined operational logic. |
| **US-03** | Epic 2 | **As a** clinic administrator,<br>**I want to** submit a scoped, time-bound consent access request for a named patient,<br>**So that** attending doctors can legally review relevant medical history for diagnostic procedures. | **High** | **5** | Involves complex multi-field form inputs, clinical taxonomy filtering, patient resolution, and state persistence. |
| **US-04** | Epic 2 | **As a** healthcare security gateway,<br>**I want to** verify requesting clinic and doctor identities against the verified-provider registry before forwarding requests to the patient,<br>**So that** impersonators, uncertified entities, or blacklisted practitioners are rejected at the perimeter. | **High** | **8** | High uncertainty and architectural complexity: involves synchronous third-party API integration, mTLS handshake, fallback caches, and strict error handling. |
| **US-05** | Epic 3 | **As a** patient,<br>**I want to** receive real-time notifications for incoming access requests and alerts 1 hour before active consent expires,<br>**So that** I stay informed and can act proactively to grant or extend permissions. | **Medium** | **3** | Event-driven webhook and mobile push notification delivery. Standard communication pattern with low architectural risk. |
| **US-06** | Epic 3 | **As a** compliance officer,<br>**I want** all consent grant, revoke, and access events permanently written to an append-only, tamper-evident audit trail,<br>**So that** legal non-repudiation, DPDP/HIPAA regulatory compliance, and post-incident forensic audits are guaranteed. | **High** | **5** | Append-only write pipeline, cryptographic checksumming/hash-chaining, and P95 latency constraint (<300ms). |

---

## 4. Sprint Simulation: Sprint 1 Execution

### 4.1 Sprint Configuration
* **Sprint Name:** `PHR Sprint 1 — Core Consent & Provider Gateway`
* **Duration:** 1 Week (Simulated Iteration)
* **Sprint Goal:** Establish end-to-end patient consent creation, immediate revocation, and provider identity verification gateway to secure core clinical workflows.
* **Committed Backlog Items (21 Story Points Total):**
  - `US-01`: Grant Time-Bound Consent (5 Points)
  - `US-02`: Real-Time Consent Revocation (3 Points)
  - `US-03`: Scoped Record Access Request (5 Points)
  - `US-04`: Provider Identity Verification Gateway (8 Points)

### 4.2 Sprint Board Lifecycle & Workflow Transitions

During the sprint simulation, issues are tracked across three key states:
1. **To Do:** Backlog items selected and committed during Sprint Planning.
2. **In Progress:** Active development, registry mock integration, and policy verification.
3. **Done:** Passed Acceptance Criteria, unit tests, code review, and definition of done (DoD).

### 4.3 Sprint 1 Completion & Backlog Rollover
* At the conclusion of Sprint 1, all 21 committed story points were completed (`Done`).
* The remaining items in the Product Backlog (`US-05`: 3 SP and `US-06`: 5 SP = 8 SP Total) are prioritized and mapped to **Sprint 2** (`PHR Sprint 2 — Notifications & Immutable Auditing`).

---

## 5. Jira Burndown Chart Analysis

### 5.1 Burndown Metrics
* **Total Story Points Committed:** 21 SP
* **Total Story Points Completed:** 21 SP
* **Scope Creep / Injected Stories:** 0 SP
* **Sprint Completion Rate:** 100%

### 5.2 Chart Trajectory Interpretation
* **Guideline (Ideal Burndown):** Displays a linear progression from 21 story points on Day 1 to 0 story points on Day 7 (reducing at a rate of 3.0 points/day).
* **Actual Remaining Value (Burndown Line):**
  - **Day 1–2:** Stable at 21 points while architectural setup and provider registry contracts were established.
  - **Day 3:** US-02 (3 SP) completed → Remaining drops to 18 SP.
  - **Day 4:** US-01 (5 SP) completed → Remaining drops to 13 SP.
  - **Day 5:** US-03 (5 SP) completed → Remaining drops to 8 SP.
  - **Day 6–7:** US-04 (8 SP) completed after rigorous integration testing → Remaining drops to 0 SP.
* **Analysis:** The actual burndown closely tracked the ideal guideline. Completing smaller, low-risk stories first established early velocity before tackling the high-complexity 8-point provider verification story.

---

## 6. Answers to Reflection Questions

### Question 1: Did your estimations reflect the actual effort?
> **Answer:**  
> Yes, the story point estimations closely reflected the actual implementation effort. By applying Planning Poker and the non-linear Fibonacci scale (1, 2, 3, 5, 8), the team separated low-uncertainty internal tasks from complex external integrations:
> - **US-02 (Revocation, 3 SP)** involved well-understood database flag updates and cache eviction, proving straightforward and completing rapidly.
> - **US-01 and US-03 (5 SP each)** required moderate effort due to validation logic, date-time calculations, and clinical taxonomy filtering.
> - **US-04 (Registry Gateway, 8 SP)** accurately captured the highest uncertainty, as it required handling external network latency, certificate validation, and edge-case error recovery.  
> Using relative estimation rather than raw hours allowed the team to account for uncertainty and architectural risk effectively.

### Question 2: Was your backlog well-prioritized?
> **Answer:**  
> Yes, the backlog was prioritized using a risk-first, value-driven Agile approach aligned with the MoSCoW method:
> - **Highest Priority (Must Haves):** US-01 through US-04 formed the foundational security and authorization layer. Without consent granting and doctor verification, the system cannot function ethically or legally. Hence, these were prioritized at the top of the backlog and scheduled into Sprint 1.
> - **Medium Priority (Should Haves):** US-05 (Real-time notifications) provides great user convenience but relies upon the underlying access request pipeline. Prioritizing it for Sprint 2 ensured the core transaction engine was verified before alert pipelines were attached.
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
> 3. **Handling Complex Items:** The 8-point story (US-04) occupied the latter half of the sprint. For future sprints, the team can consider splitting 8-point stories into smaller 3-point and 5-point stories (e.g., separating mock verification from live registry integration) to achieve an even smoother burndown curve.

---

## 7. Jira Automation Script

The script [`scripts/jira_automation.py`](./scripts/jira_automation.py) automates the creation of all Epics, User Stories, Story Points, Sprints, and workflow transitions in Atlassian Jira Cloud using the official REST API v3 and Agile API v1.0.

### Usage:
```bash
python3 scripts/jira_automation.py --token <YOUR_ATLASSIAN_API_TOKEN> --email abhsach@gmail.com --domain abhays11.atlassian.net
```
