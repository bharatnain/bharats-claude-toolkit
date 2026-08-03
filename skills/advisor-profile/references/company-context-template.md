# Company Context

*Written by the advisor-profile interview on [DATE]. Read by every C-suite advisor skill
(ceo-advisor, cfo-advisor, cmo-advisor, cpo-advisor, cro-advisor, general-counsel-advisor,
executive-mentor) before advising. Edit this file directly — if something below is wrong,
fix it here and it's fixed everywhere. Re-run the advisor-profile interview with
`--section <name>` to redo one part, or `--redo` for a full refresh.*

*Adapted from anthropics/claude-for-legal `references/company-profile-template.md` (Apache-2.0).*

---

## Who we are

**Name:** [Company name]
**Entity:** [Delaware C-corp | LLC | other]
**Industry / category:** [what space, in the user's words]
**One-liner:** [what you sell, to whom, and how it's priced]
**Stage:** [idea | pre-seed | seed | Series A | Series B+ | bootstrapped-profitable]
**Funding:** [total raised, last round, notable investors — or "bootstrapped"]
**Headcount:** [N, and rough shape — e.g., "12, mostly engineering"]

**The thing that hurts:** [what the user said hurts — write it in their words; advisors
proactively watch for it]

---

## Who's using this

**Role:** [Founder/CEO | Exec team member — which function | Operator/chief of staff | External advisor]
**Framing:** [decisions land on this user | outputs are briefing material for someone else]

---

## Business model

**Revenue model:** [subscription | usage | take-rate | services | licensing | ads | pre-revenue]
**Pricing:** [structure in one or two lines]
**Unit economics posture:** [what's known — e.g., "CAC/LTV not yet instrumented" or actual bands]

---

## Org

| Function | Owner | Notes |
|---|---|---|
| Product/Eng | [name or "founder"] | |
| Finance | [name or "no one — fractional CFO?"] | |
| Marketing | [name or gap] | |
| Sales/Revenue | [name or gap] | |
| Legal | [in-house / outside firm / gap] | |

**Hiring posture (next 12 months):** [growing / frozen / cutting — where]

---

## Financial posture

**Revenue band:** [e.g., "$1-2M ARR"] — **Growth:** [e.g., "~8% MoM"]
**Burn / runway:** [monthly burn band, months of runway]
**Margin structure:** [software-like / services-like / hardware / marketplace]
**Fundraising plans:** [next 12 months, or none]
**Numbers confidentiality:** [advisors may use detail | advisors work in bands only]

---

## GTM motion

**Primary motion:** [sales-led | product-led | channel | marketplace | community | founder-led]
**ICP:** [who buys, who uses — one or two lines]
**ACV band / price point:** [amount] — **Sales cycle:** [length]
**What actually works today:** [the channel producing customers now]
**Negotiation side (default):** [mostly selling on our paper | mostly buying on vendor paper | both]

---

## Legal and regulatory surface

**Jurisdictions:** [incorporated where; customers where; employees where]
**Regulated surface:** [GDPR / CCPA / HIPAA / PCI / fintech / minors / government — or "none identified"]
**Counsel access:** [in-house | outside firm on retainer | lawyer-when-needed | none]
**Contract posture:** [mostly our paper / mostly theirs; ~N contracts per month]
**Open matters:** [or none]

---

## Risk posture and decision rights

**Overall risk appetite:** [conservative / middle / aggressive — with exceptions noted]
**Escalation:** [who has to sign off above the user — co-founder, board, counsel — or "user decides"]
**Automatic escalations regardless of size:** [e.g., anything touching equity, personal liability, regulator contact]
**The one thing:** [the most likely cause of death in the next two years — every advisor
checks its analysis against this first]
**The question leadership always asks:** [or "not known yet"]

---

## Outputs

**Work-product header** (prepended to legal analyses generated via the general-counsel-advisor
contract-review references; other advisors omit it):

- If counsel access is in-house or retained and the user works with them: `PRIVILEGED & CONFIDENTIAL — PREPARED AT THE DIRECTION OF COUNSEL`
- Otherwise: `RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED ATTORNEY BEFORE ACTING`

---

## Contract playbook

*Optional — used by the general-counsel-advisor contract-review references (NDA triage,
vendor/SaaS agreement review). Sales-side = we sell; our paper. Purchasing-side = we buy;
vendor paper. Never apply one side's position to the other side's contract.*

**Active side:** [sales / purchasing / both / not configured]

### Sales-side playbook

*[Not configured — run the advisor-profile interview (--section legal) to build it]*

<!-- When configured, each side carries: Limitation of liability (standard / fallbacks /
never accept / carveouts), Indemnification, Data protection, Term and termination,
Governing law and venue, NDA triage positions, SaaS positions, AI/ML training rights,
and The one thing (the per-side deal-breaker checked first in every review). -->

### Purchasing-side playbook

*[Not configured — run the advisor-profile interview (--section legal) to build it]*

---

## Review preferences

confirm_routing: true   # Set to false to skip contract-review routing confirmation

---

## NDA triage preferences

closing_action: "[standing instruction appended to every NDA triage output — e.g.,
'Forward this output and the NDA to our outside counsel.' Leave unset for the default.]"

---

## Playbook monitor settings

pattern_threshold: 5    # deviations on the same clause before a playbook update is proposed
lookback_months: 12     # rolling window for pattern detection

---

## Seed documents reviewed

| Document | Date | What it contributed |
|---|---|---|
| [pitch deck / board deck / model / site] | [date] | [facts extracted, deltas found] |

---

*To re-run the interview: ask for the advisor-profile skill with `--redo` (full, diff shown
first) or `--section <business-model|org|financials|gtm|legal|risk>` (one section only).*
