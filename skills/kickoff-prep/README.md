# onboarding.kickoff-prep

Prepare for an onboarding kickoff — generates a customized customer-facing agenda and an internal pre-kickoff checklist. Reads kickoff format, required attendees, onboarding model, and milestone targets from the onboarding profile. Pulls account context from CRM if available.

## Use it for

- Customer-facing agenda and internal prep checklist together (--prep, default)
- Customer-facing agenda only (--agenda)
- Internal prep checklist only (--checklist)

## Don't use it for

- Post-kickoff plan generation (use onboarding-plan --draft)
- Sending the agenda to the customer

## How to trigger it

Say something like:

- "kickoff prep"
- "prepare kickoff"
- "kickoff agenda"
- "kickoff checklist"

## What you get

- Customer-facing kickoff agenda draft
- Internal pre-kickoff preparation checklist

## Prerequisites

- onboarding CLAUDE.md (kickoff format, required attendees, onboarding model)

## Governance

- Agenda is a draft only — no autonomous send to customer
- Attendee requirements sourced from profile

## See also

- onboarding.onboarding-plan
- onboarding.success-criteria

---

*Domain: `onboarding` · Skill ID: `onboarding.kickoff-prep`*
