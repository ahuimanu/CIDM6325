# Product Requirements Document PRD Student Athlete Management System SAMS

## 1. Document Information

* Product/Feature Name: Student Athlete Management System (SAMS)
* Author(s): Zane Hill
* Date Created: 2025-09-19
* Last Updated: 2025-09-21
* Version: 0.1 Draft

---

## 2. Overview

* Summary: SAMS is a role-based web application that centralizes team schedules, athlete availability, and attendance logging for collegiate programs. It resolves fragmented communication across texts, spreadsheets, and calendar invites by offering a single source of truth with conflict detection against course schedules, notifications for changes, and exportable attendance. Phase one focuses on reliability and clarity before expanding to performance analytics or recruiting.
* Problem Statement: Collegiate teams coordinate practices, lifts, travel, games, study halls, rehab, compliance sessions, and academics across multiple facilities and time zones. The current patchwork of tools leads to missed events, double-bookings, late compliance paperwork, and uneven communication, especially for injured or traveling athletes. SAMS reduces conflicts and improves communication by unifying schedules and role-based workflows.

* Goals & Objectives:

  * Deliver an accurate calendar with recurring events, locations, and notes.
  * Detect and surface event↔class conflicts per athlete at creation and in daily views.
  * Provide dependable notifications and acknowledgements of changes.
  * Log attendance with quick input and CSV export per event.
  * Achieve targeted adoption and reliability metrics in the first two weeks.

* Non-Goals:

  * Athletic performance telemetry and workload analytics.
  * Recruiting CRM and prospect management.
  * Grade ingestion or deep academic analytics.
  * Native mobile app; payments or e‑commerce.

---

## 3. Context & Background

* Business Context: Aligns with departmental goals to improve operational reliability, compliance readiness, and time management for student-athletes. Supports OKRs around reducing conflicts, improving attendance tracking, and increasing communication clarity.
* Market/Customer Insights: Primary users are Coaches, Athletes, Athletic Trainers/Staff, and Compliance/Academics. They need real-time, reliable schedules, conflict visibility, and auditable activity logs. Registrars/IT may integrate course schedules and SSO. Parents/Supporters may require read-only calendars.
* Competitive/Benchmark References: Existing point tools offer calendars or messaging but lack integrated conflict detection against academic schedules and role-based attendance workflows. SAMS differentiates via academic conflict checks and simple exports.

---

## 4. Scope

* In Scope:

  * Team calendar and events (single/recurring), with location and notes.
  * Availability blocks per athlete (class schedules) and conflict detection.
  * Notifications via email and in-app; per-user iCalendar feed (.ics).
  * Attendance logging (present/late/absent) and CSV export.
  * Role-based views and permissions: Coach, Athlete, Staff; Admin for roster and season setup.

* Out of Scope:

  * Native mobile apps and push notifications to mobile OS.
  * Performance analytics, GPS/fitness integrations, recruiting features.
  * Grade ingestion and deep academic analytics.
  * Payments and e‑commerce.

---

## 5. User Stories & Use Cases

* Primary User Persona(s):

  * Coach: Publishes schedules, monitors conflicts, records attendance, messages groups.
  * Athlete: Sees personal schedule, acknowledges changes, uploads/updates class times.
  * Staff Athletic Trainer Manager: Marks limited/rehab status notes; views availability.
  * Compliance Academic Staff: Reviews activity logs and exports for audits.
  * Admin Registrar IT: Seeds seasons, manages rosters, configures integrations.

* User Stories:

  * As a Coach, I want to create recurring events with locations so that my team has a reliable calendar.
  * As a Coach, I want to see conflicts at a glance so that I can adjust times or rosters.
  * As an Athlete, I can upload or confirm my class schedule so that conflicts are detected automatically.
  * As an Athlete, I want email notifications and an .ics feed so that my calendar stays in sync.
  * As Staff, I can record attendance quickly so that reports are accurate after events.
  * As Compliance staff, I can export attendance logs so that I can satisfy audits.
  * As Admin, I can manage rosters and seasons so that the system reflects current teams.

* Use Case Scenarios:

  * Happy Path: Coach creates a recurring practice. System checks athlete class blocks and flags conflicts. Athletes receive notification, acknowledge changes, and their personal .ics updates. After practice, Staff records attendance and exports CSV.
  * Edge Case 1: Athlete has missing class data. System displays an "unknown availability" banner to athlete and coach until filled; event creation still succeeds with warnings.
  * Edge Case 2: Last-minute venue/time change within 24h. System sends immediate notifications and requires athlete acknowledgement; dashboard highlights unacknowledged changes.

---

## 6. Functional Requirements

* FR-001 Authentication and Roles: Support user accounts with roles Coach, Athlete, Staff, Admin; only Admin can manage seasons and rosters.
* FR-002 Event CRUD: Create, read, update, delete team events with start/end, location, notes.
* FR-003 Recurrence: Support recurring rules (daily, weekly with BYDAY) and exceptions.
* FR-004 Calendar Views: Team view and per-user personal view; time zone aware.
* FR-005 Availability Input: Athletes can add class blocks manually and via CSV import template.
* FR-006 Conflict Detection: On event create/update, flag athlete conflicts vs. class blocks; show counts and lists.
* FR-007 Conflict Surfaces: Athlete and Coach dashboards display conflict banners until resolved.
* FR-008 Notifications Email: Send emails on event create/update/cancel; include summary and deep link.
* FR-009 In-App Alerts: Show in-app notifications; track read state and acknowledgement.
* FR-010 Acknowledgements: Athletes can acknowledge changes; coach sees acknowledgement rate per event.
* FR-011 Attendance Logging: Staff marks present/late/absent per athlete; bulk actions supported.
* FR-012 Attendance Export: Export per-event CSV including timestamp, status, and notes.
* FR-013 ICS Feeds: Provide a secure per-user .ics feed that includes team events filtered by role/roster.
* FR-014 Roster Management: Admin adds/removes athletes and assigns them to teams and seasons.
* FR-015 Audit Log: Record who created/edited/deleted events and who marked attendance.
* FR-016 Accessibility: All interactive features are fully keyboard navigable and screen-reader friendly.

---

## 7. Non-Functional Requirements

* Performance: p95 page load ≤800 ms on team calendar; p95 event create/update ≤400 ms; notifications dispatch within 30 s.
* Scalability: Support 5 teams, each up to 100 athletes, 1,000 active events per season; 10 req/s sustained, 50 peak.
* Accessibility: WCAG 2.1 AA targets including color contrast, focus order, and ARIA labels.
* Security/Compliance: Role-based access control; HTTPS/TLS; at-rest encryption for PII; audit logs; FERPA-aligned handling of educational records; exclude health data and PHI in Phase 1.
* Reliability/Availability: Target 99.5% uptime for MVA; graceful degradation showing cached calendar if backend is unavailable; retry and dead-letter for notification jobs.
* Privacy: Consent prompts for .ics sharing; ability to revoke feeds; minimal data retention policies; clear privacy notice.

---

## 8. Dependencies

* Internal: User/auth service; team and roster directory; notification job queue; relational database.
* External APIs/Standards: Email SMTP or transactional email API; iCalendar RFC 5545 for .ics; optional SSO (SAML/OIDC) in later phase; CSV import/export.
* Cross-Team Deliverables: Registrar data access for class schedules via CSV export; IT coordination for SSO if pursued; compliance review for audit log format.

---

## 9. Risks & Assumptions

* Risks:

  * Privacy and compliance risks handling educational records. Mitigation: strict RBAC, audit logs, encryption, consent, and retention limits.
  * Incomplete or late class data causing persistent conflicts. Mitigation: CSV templates, required onboarding steps, and unresolved-conflict banners.
  * Scope creep (mobile app, recruiting, analytics). Mitigation: freeze core flows, review gates tied to metrics, public backlog for deferrals.
  * Adoption risk if notifications are noisy. Mitigation: sensible defaults, digest options, acknowledgement tracking.

* Assumptions:

  * Teams can provide class schedules via CSV within the first week.
  * Email delivery is acceptable in Phase 1; mobile push not required.
  * One environment serves pilot teams with moderate concurrency.

---

## 10. Acceptance Criteria

* FR-002/FR-003: A coach can create a weekly recurring event with location and notes; event appears on team and personal views within 2 s; updating time sends notifications within 30 s; recurrence exceptions are honored.
* FR-005/FR-006: When an athlete imports a CSV with class blocks, creating a practice overlapping a class flags the athlete as conflicted and shows total conflict count before save.
* FR-008/FR-009/FR-010: On event update within 24 h, athletes receive an email and see an in-app alert; at least 80% of roster acknowledgements are recorded within 12 h on test data.
* FR-011/FR-012: Staff can mark attendance for a roster of 40 athletes in under 2 minutes using bulk actions; CSV export downloads with correct headers and statuses.
* FR-013: Each user can subscribe to a unique .ics URL; revoking the feed invalidates previous URLs within 60 s.
* FR-014/FR-015: Admin changes to rosters and events are recorded with user, timestamp, and action; logs are queryable by date range.
* FR-016: All primary flows are keyboard navigable, pass automated contrast checks, and provide descriptive labels.

---

## 11. Success Metrics

* Schedule reliability: ≥95% of events published ≥24 h before start; ≤2% last‑minute unacknowledged changes.
* Conflict reduction: ≥50% drop in event↔class conflicts after week 2, tracked per athlete.
* Engagement: ≥80% athlete 7‑day active rate; ≥90% of events with recorded attendance.
* Communication clarity: ≥75% of athletes enable calendar sync; notification open rate ≥60%.

---

## 12. Rollout & Release Plan

* Phasing:

  * MVP MVA Weeks 1–2: Calendar CRUD, recurrence, notifications, attendance, CSV class import, conflicts, .ics feeds.
  * Iteration 2 Weeks 3–4: UX refinements, acknowledgement dashboards, improved exports, admin guardrails.
  * Future: SSO, registrar integrations, limited status notes, reporting, mobile app exploration.

* Release Channels: Pilot with one team, then expand to 2–3 teams as a staged rollout; GA after metrics meet targets.
* Training/Documentation Needs: Quick-start guides for each role; CSV templates with examples; accessibility notes; support FAQ; incident and change logs.

---

## 13. Open Questions

* Which SSO provider and timeline if adopted SAML vs OIDC?
* Minimum data set for class blocks course code vs time-only; ownership of updates during add drop periods?
* Required acknowledgement thresholds and escalation rules for changes within 24 h?
* Do compliance users need CARA-specific reports in Phase 1 or only raw attendance exports?
* Should .ics feeds include private location notes or exclude sensitive notes by default?

---

## 14. References

* Project Pitch source and success metrics, role definitions, and scope.
* Standards and guidance: RFC 5545 iCalendar, WCAG 2.1, FERPA, NCAA CARA.
* Educause, Carnegie, NATA resources on student-athlete scheduling and well-being.



## EXPLICIT AI DISCLOSURE - ZANE HILL - MODULE 2 ASSIGNMENT FOR SAMS-PRD

OpenAI. (2025, September 21). ChatGPT (GPT-5) [Large language model]. Prompts and responses provided to Zane Hill for drafting the Product Requirements Document (PRD) in CIDM 6325. OpenAI. https://chat.openai.com - Files Included: Zane Hill - Module 1 - Project Pitch.docx - "Can you create a PRD for this project? Here is the PRD Template. Please use this and complete it. Do not miss a section. Fill every point based off of the Project Pitch. Take your time on this assignment and take time to think so every point is completed." GPT Utilized to assist in creation and full documentaiton of PRD document based off of the project guidelines for the Student-Athlete-Management-System (SAMS). Completed personal review, revision and documentation. GPT Assisted in establishing a framework for this assignment. All information is property of Zane Hill for the purpose of CIDM 6325, Babb.