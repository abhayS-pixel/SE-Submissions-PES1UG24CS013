#!/usr/bin/env python3
"""
Jira Cloud Automation Script for SE Lab 2: Agile Backlog Creation & Sprint Simulation
Problem Statement #13: Patient Health Record Consent Management System
PES University - Dept. of CSE
"""

import sys
import os
import json
import base64
import argparse
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timedelta

ctx = ssl._create_unverified_context()


def get_auth_header(email, token):
    raw = f"{email}:{token}".encode("utf-8")
    encoded = base64.b64encode(raw).decode("utf-8")
    return {"Authorization": f"Basic {encoded}", "Content-Type": "application/json", "Accept": "application/json"}

def jira_request(method, url, headers, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            return status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            parsed = json.loads(err_body)
        except Exception:
            parsed = err_body
        return e.code, parsed

def make_adf_description(text):
    paragraphs = text.strip().split("\n\n")
    content = []
    for p in paragraphs:
        content.append({
            "type": "paragraph",
            "content": [{"type": "text", "text": p.strip()}]
        })
    return {"type": "doc", "version": 1, "content": content}

def find_story_points_field(base_url, headers):
    status, fields = jira_request("GET", f"{base_url}/rest/api/3/field", headers)
    if status == 200 and isinstance(fields, list):
        for f in fields:
            name = f.get("name", "").lower()
            if "story point" in name or "estimate" in name:
                return f.get("id")
    return "customfield_10016"

def main():
    parser = argparse.ArgumentParser(description="Automate Jira setup for SE Lab 2")
    parser.add_argument("--domain", default="abhays11.atlassian.net", help="Jira domain")
    parser.add_argument("--email", default="abhsach@gmail.com", help="Atlassian account email")
    parser.add_argument("--token", required=True, help="Atlassian API token")
    parser.add_argument("--project-name", default="Patient Health Record Consent Management System", help="Project name")
    parser.add_argument("--project-key", default="PHR", help="Project Key (uppercase)")

    args = parser.parse_args()
    base_url = f"https://{args.domain.replace('https://', '').strip('/')}"
    headers = get_auth_header(args.email, args.token)

    print(f"[*] Connecting to Jira Cloud: {base_url} as {args.email}...")

    # 1. Verify Authentication
    status, user_info = jira_request("GET", f"{base_url}/rest/api/3/myself", headers)
    if status != 200:
        print(f"[-] Authentication failed (HTTP {status}): {user_info}")
        sys.exit(1)
    print(f"[+] Authenticated successfully as: {user_info.get('displayName')} ({user_info.get('emailAddress')})")
    account_id = user_info.get("accountId")

    # 2. Check or Create Project
    status, projects = jira_request("GET", f"{base_url}/rest/api/3/project/search", headers)
    project = None
    if status == 200 and "values" in projects:
        for p in projects["values"]:
            if p["key"] == args.project_key or p["name"].lower() == args.project_name.lower():
                project = p
                break

    if project:
        print(f"[+] Using existing project: {project['name']} (Key: {project['key']}, ID: {project['id']})")
        project_key = project["key"]
        project_id = project["id"]
    else:
        print(f"[*] Creating new Scrum project: {args.project_name} (Key: {args.project_key})...")
        proj_payload = {
            "key": args.project_key,
            "name": args.project_name,
            "projectTypeKey": "software",
            "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic",
            "description": "Lab 2: Patient Health Record Consent Management System",
            "leadAccountId": account_id
        }
        status, new_proj = jira_request("POST", f"{base_url}/rest/api/3/project", headers, proj_payload)
        if status not in (200, 201):
            proj_payload["projectTemplateKey"] = "com.pyxis.greenhopper.jira:gh-scrum-template"
            status, new_proj = jira_request("POST", f"{base_url}/rest/api/3/project", headers, proj_payload)
            if status not in (200, 201):
                print(f"[-] Failed to create project automatically: {new_proj}")
                if "values" in projects and len(projects["values"]) > 0:
                    project = projects["values"][0]
                    project_key = project["key"]
                    project_id = project["id"]
                    print(f"[+] Falling back to existing project: {project_key}")
                else:
                    sys.exit(1)
            else:
                project_key = new_proj.get("key", args.project_key)
                project_id = new_proj.get("id")
        else:
            project_key = new_proj.get("key", args.project_key)
            project_id = new_proj.get("id")
            print(f"[+] Project created successfully! Key: {project_key}")

    # 3. Find Board
    status, boards = jira_request("GET", f"{base_url}/rest/agile/1.0/board?projectKeyOrId={project_key}", headers)
    board_id = None
    if status == 200 and "values" in boards and len(boards["values"]) > 0:
        board = boards["values"][0]
        board_id = board["id"]
        print(f"[+] Located Agile Scrum Board: {board['name']} (Board ID: {board_id})")
    else:
        status, all_boards = jira_request("GET", f"{base_url}/rest/agile/1.0/board", headers)
        if status == 200 and "values" in all_boards and len(all_boards["values"]) > 0:
            board_id = all_boards["values"][0]["id"]
            print(f"[+] Located Board: {all_boards['values'][0]['name']} (Board ID: {board_id})")

    # 4. Find Story Points field
    sp_field = find_story_points_field(base_url, headers)
    print(f"[+] Story Points field identified as: {sp_field}")

    # 5. Define Epics
    epics_data = [
        {
            "summary": "Epic 1: Patient Consent Administration & Granular Permissions",
            "description": "Provide patients with autonomous, granular controls to grant, configure, and instantly revoke time-bounded consent for their electronic medical history (FR-001, FR-002)."
        },
        {
            "summary": "Epic 2: Healthcare Provider Scoped Access & Identity Verification",
            "description": "Enable clinic administrators to request scoped access to diagnostic records while enforcing strict cryptographic and registry-based doctor/clinic verification at the system boundary (FR-003, FR-004)."
        },
        {
            "summary": "Epic 3: Real-Time Alerts & Immutable Audit Trail",
            "description": "Deliver immediate notification alerts to patients for new requests and approaching consent expirations, backed by an immutable, append-only audit trail meeting strict performance and security thresholds (FR-005, NFR-001, NFR-002)."
        }
    ]

    created_epics = {}
    print("\n[*] Creating Epics...")
    for epic in epics_data:
        epic_payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": epic["summary"],
                "description": make_adf_description(epic["description"]),
                "issuetype": {"name": "Epic"}
            }
        }
        status, res = jira_request("POST", f"{base_url}/rest/api/3/issue", headers, epic_payload)
        if status in (200, 201):
            epic_key = res["key"]
            created_epics[epic["summary"].split(":")[0].strip()] = epic_key
            print(f"  [+] Created {epic['summary'].split(':')[0]}: {epic_key} - {epic['summary']}")
        else:
            print(f"  [-] Failed to create Epic '{epic['summary']}': {res}")

    # 6. Define User Stories
    stories_data = [
        {
            "epic": "Epic 1",
            "id": "US-01",
            "title": "US-01: Grant Time-Bound Consent",
            "story": "As a patient, I want to grant time-bounded (e.g., 24-hour) access permissions for specific diagnostic records to verified clinic doctors, so that my sensitive medical history is accessible only during my active consultation and auto-revoked thereafter.",
            "acceptance": "Pass: Clinic access automatically revokes upon expiry timestamp.\nFail: Clinic accesses records after consent expiration.",
            "points": 5,
            "priority": "High",
            "sprint": 1
        },
        {
            "epic": "Epic 1",
            "id": "US-02",
            "title": "US-02: Real-Time Consent Revocation",
            "story": "As a patient, I want to revoke previously granted consent at any time before its natural expiry with immediate effect, so that clinics or doctors are instantly blocked if my consultation terminates early or circumstances change.",
            "acceptance": "Pass: Access attempt made 1 second after manual revocation is denied and logged.\nFail: Clinic/lab retains or regains access after patient revokes consent.",
            "points": 3,
            "priority": "High",
            "sprint": 1
        },
        {
            "epic": "Epic 2",
            "id": "US-03",
            "title": "US-03: Scoped Record Access Request",
            "story": "As a clinic administrator, I want to submit a scoped, time-bound consent access request for a named patient, so that attending doctors can legally review relevant medical history for diagnostic procedures.",
            "acceptance": "Pass: Request specifies scope, required records, and duration, and is delivered to patient.\nFail: Missing mandatory clinical metadata or patient identifier accepted.",
            "points": 5,
            "priority": "High",
            "sprint": 1
        },
        {
            "epic": "Epic 2",
            "id": "US-04",
            "title": "US-04: Provider Identity Verification Gateway",
            "story": "As a healthcare security gateway, I want to verify requesting clinic and doctor identities against the verified-provider registry before forwarding requests to the patient, so that impersonators or unverified entities are rejected at the perimeter.",
            "acceptance": "Pass: Verified doctor active in registry allows request propagation.\nFail: Suspended or invalid doctor credentials allow request delivery.",
            "points": 8,
            "priority": "High",
            "sprint": 1
        },
        {
            "epic": "Epic 3",
            "id": "US-05",
            "title": "US-05: Real-Time Alerts & Expiry Reminders",
            "story": "As a patient, I want to receive real-time notifications for incoming access requests and alerts 1 hour before active consent expires, so that I stay informed and can act proactively to grant or extend permissions.",
            "acceptance": "Pass: Patient receives push notification within 2 seconds of clinic request submission and 1 hour before expiry.\nFail: Notification drops or arrives after consent has lapsed.",
            "points": 3,
            "priority": "Medium",
            "sprint": 2
        },
        {
            "epic": "Epic 3",
            "id": "US-06",
            "title": "US-06: Append-Only Immutable Audit Trail",
            "story": "As a compliance officer, I want all consent grant, revoke, and access events permanently written to an append-only, tamper-evident audit trail, so that legal non-repudiation, DPDP/HIPAA regulatory compliance, and post-incident forensic audits are guaranteed.",
            "acceptance": "Pass: All events logged with cryptographic timestamp under 300ms latency; log cannot be mutated.\nFail: Any audit trail record can be updated, deleted, or truncated.",
            "points": 5,
            "priority": "High",
            "sprint": 2
        }
    ]

    created_stories = []
    print("\n[*] Creating User Stories & Assigning Story Points (Fibonacci Scale)...")
    for s in stories_data:
        parent_epic_key = created_epics.get(s["epic"])
        description_text = f"USER STORY:\n{s['story']}\n\nACCEPTANCE CRITERIA:\n{s['acceptance']}\n\nSTORY POINTS: {s['points']} (Fibonacci Scale)"
        fields = {
            "project": {"key": project_key},
            "summary": s["title"],
            "description": make_adf_description(description_text),
            "issuetype": {"name": "Story"},
            "priority": {"name": s["priority"]}
        }
        if parent_epic_key:
            fields["parent"] = {"key": parent_epic_key}
        if sp_field:
            fields[sp_field] = s["points"]

        status, res = jira_request("POST", f"{base_url}/rest/api/3/issue", headers, {"fields": fields})
        if status not in (200, 201) and sp_field in fields:
            del fields[sp_field]
            status, res = jira_request("POST", f"{base_url}/rest/api/3/issue", headers, {"fields": fields})

        if status in (200, 201):
            story_key = res["key"]
            s["jira_key"] = story_key
            created_stories.append(s)
            print(f"  [+] Created {s['id']}: {story_key} | {s['title']} | Points: {s['points']} | Priority: {s['priority']}")
        else:
            print(f"  [-] Failed to create {s['id']}: {res}")

    if not board_id:
        print("[-] Board ID not found, skipping Sprint simulation API calls.")
        return

    print("\n[*] Setting up Sprints on Scrum Board...")
    now = datetime.utcnow()
    end_sprint1 = now + timedelta(days=7)

    sprint1_payload = {
        "name": "PHR Sprint 1",
        "startDate": now.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "endDate": end_sprint1.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "originBoardId": board_id,
        "goal": "Implement core patient consent granting, revocation, and provider verification gateway (FR-001, FR-002, FR-003, FR-004)"
    }
    status, sprint1 = jira_request("POST", f"{base_url}/rest/agile/1.0/sprint", headers, sprint1_payload)
    if status in (200, 201):
        sprint1_id = sprint1["id"]
        print(f"[+] Created Sprint 1: '{sprint1['name']}' (ID: {sprint1_id})")

        sprint1_keys = [s["jira_key"] for s in created_stories if s.get("sprint") == 1 and "jira_key" in s]
        if sprint1_keys:
            jira_request("POST", f"{base_url}/rest/agile/1.0/sprint/{sprint1_id}/issue", headers, {"issues": sprint1_keys})
            print(f"[+] Moved {len(sprint1_keys)} stories into Sprint 1: {', '.join(sprint1_keys)}")

        start_payload = {
            "state": "active",
            "startDate": now.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "endDate": end_sprint1.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
        status, _ = jira_request("POST", f"{base_url}/rest/agile/1.0/sprint/{sprint1_id}", headers, start_payload)
        if status in (200, 204):
            print("[+] Sprint 1 STARTED! Duration: 1 week.")

        print("\n[*] Simulating Sprint Progress (Moving tasks across To Do -> In Progress -> Done)...")
        for key in sprint1_keys:
            status, trans_data = jira_request("GET", f"{base_url}/rest/api/3/issue/{key}/transitions", headers)
            if status == 200 and "transitions" in trans_data:
                done_trans = None
                for t in trans_data["transitions"]:
                    if t["name"].lower() in ("done", "closed", "resolved", "complete"):
                        done_trans = t
                        break
                if done_trans:
                    jira_request("POST", f"{base_url}/rest/api/3/issue/{key}/transitions", headers, {"transition": {"id": done_trans["id"]}})
                    print(f"  [+] Transitioned {key} to DONE")
                else:
                    first_t = trans_data["transitions"][0]
                    jira_request("POST", f"{base_url}/rest/api/3/issue/{key}/transitions", headers, {"transition": {"id": first_t["id"]}})
                    print(f"  [+] Transitioned {key} to {first_t['name']}")

        status, _ = jira_request("POST", f"{base_url}/rest/agile/1.0/sprint/{sprint1_id}", headers, {"state": "closed"})
        if status in (200, 204):
            print("[+] Sprint 1 COMPLETED! Burndown chart generated.")

    sprint2_payload = {
        "name": "PHR Sprint 2",
        "originBoardId": board_id,
        "goal": "Implement real-time patient alerts and append-only audit trail logging (FR-005, NFR-001, NFR-002)"
    }
    status, sprint2 = jira_request("POST", f"{base_url}/rest/agile/1.0/sprint", headers, sprint2_payload)
    if status in (200, 201):
        sprint2_id = sprint2["id"]
        print(f"[+] Created Sprint 2: '{sprint2['name']}' (ID: {sprint2_id})")
        sprint2_keys = [s["jira_key"] for s in created_stories if s.get("sprint") == 2 and "jira_key" in s]
        if sprint2_keys:
            jira_request("POST", f"{base_url}/rest/agile/1.0/sprint/{sprint2_id}/issue", headers, {"issues": sprint2_keys})
            print(f"[+] Moved {len(sprint2_keys)} stories into Sprint 2: {', '.join(sprint2_keys)}")

    print("\n=======================================================")
    print("           JIRA LAB 2 SETUP COMPLETE!                  ")
    print("=======================================================")
    print(f"Project Name: {args.project_name}")
    print(f"Project Key:  {project_key}")
    print(f"Jira Board:   {base_url}/jira/software/c/projects/{project_key}/boards/{board_id}")
    print(f"Backlog URL:  {base_url}/jira/software/c/projects/{project_key}/boards/{board_id}/backlog")
    print(f"Reports URL:  {base_url}/jira/software/c/projects/{project_key}/boards/{board_id}/reports/burndown-chart")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
