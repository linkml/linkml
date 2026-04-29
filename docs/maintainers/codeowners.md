# CODEOWNERS

The LinkML monorepo contains many generators, validators, and subsystems —
too many for any single person to review competently. The
[`.github/CODEOWNERS`](https://github.com/linkml/linkml/blob/main/.github/CODEOWNERS)
file is how we route PRs to the people who actually maintain each area.

For the underlying GitHub mechanics, see the upstream
[CODEOWNERS documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
This page only covers how LinkML uses it.

## The LinkML model: opt-in stewardship

LinkML uses an **opt-in** model. The `CODEOWNERS` file contains:

- **No default (`*`) rule.** Paths that no one has claimed are reviewed
  normally, exactly as they were before CODEOWNERS existed. CODEOWNERS does
  not create a new approval gate for the rest of the codebase.
- **Per-generator / per-subsystem rules** for specific directories (e.g.
  `packages/linkml/src/linkml/generators/pydanticgen/`,
  `packages/linkml/src/linkml/generators/yarrrmlgen.py`) where a contributor
  has explicitly volunteered to steward the code. The baseline for
  identifying candidate stewards per generator is
  [Generator and Validator Governance](generator-governance.md), which
  records contributor history from `git blame`.
- **Governance rules** — `CODEOWNERS` itself and the governance documents in
  `docs/maintainers/` are owned by `@linkml/core-team` to prevent accidental
  self-appointments.

Implications:

- Being listed in `CODEOWNERS` does **not** grant repository write access.
  Write access comes from
  [team membership](contributor-hierarchy.md) (`developers-collaborators`,
  `core-team`, or `admin`).
- Being listed **does** make your approval required on PRs touching your
  paths (subject to the [1-month fallback](#avoiding-review-bottlenecks-the-1-month-fallback)
  below).
- Where possible, each rule should list **at least two people** so review is
  not blocked when one steward is unavailable.

### Expectations of CODEOWNERS

Being a CODEOWNER is stewardship on behalf of the wider LinkML community,
not personal ownership of "your" code. CODEOWNERS are expected to:

- **Act in the interest of the broader LinkML community** — its users,
  downstream packages, and the long-term cohesion of the project — and not
  only their own technical preferences for an area.
- **Develop in line with LinkML's design principles.** Where the project has
  established architectural directions (the meta-model, generator interfaces,
  validation semantics, schema-driven workflows), changes in your area should
  remain consistent with them. Disagreement with a direction is welcome, but
  it should be argued in the open and resolved through governance — not
  enforced through quiet vetoes.
- **Engage constructively with proposals from the wider project**, including
  ones you would not have written yourself, when they are consistent with the
  project's direction.

A structural check on these expectations is built into the workflow: **no one
can merge their own PR.** CODEOWNER approval and the act of merging are
deliberately separated, so neither a CODEOWNER nor any single core developer
can unilaterally push a direction without engagement from at least one other
reviewer. The mechanisms below — the 1-month fallback, the project-direction
override, and the stepping-down process — exist within that frame.

## Avoiding review bottlenecks: the 1-month fallback

CODEOWNERS is a stewardship signal, **not a veto**. If CODEOWNERS become
unresponsive, the project must still be able to move. The following fallback
applies to every path with a CODEOWNER:

> **If no CODEOWNER has reviewed a PR within one month of review being
> requested, any member of the
> [`core-team`](https://github.com/orgs/linkml/teams/core-team) may approve
> and merge it.**

Details:

- **Clock start.** The month starts when review is formally requested —
  typically when the PR is opened in a non-draft state, or when it is moved
  out of draft and a CODEOWNER is auto-requested as reviewer. Pushing new
  commits does not reset the clock.
- **What counts as "review".** Any substantive review activity by a
  CODEOWNER counts: an approval, a "changes requested" review, or review
  comments that engage with the content of the PR. A single "LGTM" without
  looking counts; a thumbs-up reaction does not.
- **Good-faith escalation.** Before invoking the fallback, the PR author (or
  an interested core developer) should ping the CODEOWNER at least once in
  the PR and wait a few days. If there is still no response, the fallback
  applies.
- **Who can invoke it.** Any member of `core-team` can provide the fallback
  approval. They do not need to be the PR author. They are expected to do a
  normal substantive review — the fallback removes the *requirement* for
  CODEOWNER approval, not the need for *some* informed approval.
- **Scope.** The fallback applies to review approval only. It does not grant
  write access, does not bypass branch protection rules, and does not alter
  the CODEOWNERS file itself.
- **Intent.** The goal is to prevent stalled PRs, not to route around
  stewards. When the fallback is used, the CODEOWNER remains the CODEOWNER;
  they may still push back on the merge via follow-up issues or revert PRs
  if they believe the change was wrong.

If a CODEOWNER consistently cannot meet the 1-month window, consider stepping
down (see [Stepping down](#stepping-down)) or adding co-owners so that
review is not dependent on a single person.

### Implementation note

GitHub's branch protection cannot enforce a time-based fallback automatically:
if "Require review from Code Owners" is enabled, CODEOWNER approval is
required indefinitely. To make this policy effective in GitHub's UI, an
[admin](contributor-hierarchy.md) may temporarily remove the CODEOWNER
requirement for a specific PR once the month has elapsed, or the policy may
be encoded in a bot in the future. Until then, the policy is honour-based:
core developers should invoke it sparingly and transparently.

## When project direction and a CODEOWNER disagree

CODEOWNERS exist to ensure technical review by someone familiar with an
area; they are not a veto over the project's overall direction. From time to
time the project will need to make a change that a CODEOWNER opposes — a
coordinated change across generators, a deprecation, a meta-model evolution,
or a course correction in how an area is built. The following escape hatches
apply, in order of preference:

1. **Discussion first.** Most disagreements resolve when both sides
   articulate the underlying design principle and trade-off explicitly, in
   the PR or in a linked governance issue. CODEOWNERS, the PR author, and
   any interested core developers should engage at this level before
   escalating.
2. **Core-team override.** If discussion does not produce convergence and
   the change is consistent with documented LinkML design principles, the
   [`core-team`](https://github.com/orgs/linkml/teams/core-team) may approve
   and merge the PR over the CODEOWNER's objection. The objection is recorded
   in the PR — it is not erased — and the CODEOWNER may follow up with a
   revert PR or a governance issue if they believe the change was wrong.
3. **Realignment of stewardship.** If the misalignment between a CODEOWNER
   and the project's direction is persistent across many PRs in an area,
   repeated case-by-case overrides become a poor substitute for a clear
   stewardship arrangement. The appropriate response is to revisit ownership
   of the area; see [Stepping down](#stepping-down).

Like the 1-month fallback, this escape hatch is intended to keep the project
moving, not to route around stewards. CODEOWNERS retain their role and their
voice; what the override removes is the ability for a single person to
indefinitely block a change the wider project supports. Combined with the
no-self-merge rule, the result is symmetrical: neither a CODEOWNER nor the
core team can push a direction through an owned area without substantive
engagement from someone else.

## How to ascend to CODEOWNER status

Being a CODEOWNER is how a collaborator grows into reviewing and merging
authority in a specific area. It is the primary path between
["collaborator"](contributor-hierarchy.md) and ["core developer"](contributor-hierarchy.md).

### Prerequisites

Before requesting CODEOWNER status for an area, you should:

1. Be a member of the
   [`developers-collaborators`](https://github.com/orgs/linkml/teams/developers-collaborators)
   team. If you are not yet, see the
   [contributor hierarchy](contributor-hierarchy.md) for how to join.
2. Have a track record of **sustained, quality contributions** to the area in
   question. There is no hard number, but a rough guide:
   - At least a few merged PRs touching the area
   - At least one non-trivial feature, bugfix, or refactor that required
     understanding the area's internals
   - Ideally, you have already reviewed others' PRs in the area informally
3. Be willing to **respond to review requests** in a reasonable timeframe. If
   no CODEOWNER engages with a PR within one month, any core-team member may
   approve and merge it (see
   [Avoiding review bottlenecks](#avoiding-review-bottlenecks-the-1-month-fallback)).
   If your availability is limited, say so — we can still add you, but it
   helps to know, and you may want a co-owner to share the load.

### The process

No separate request issue — just open a PR.

1. Open a PR against `.github/CODEOWNERS` adding yourself (and ideally a
   co-owner) to the relevant path(s).
2. In the PR description, include:
   - **Links to at least three merged PRs** in the area that justify
     codeownership. These should be non-trivial contributions that
     demonstrate you understand the area's internals.
   - A brief statement of what you intend to do as a CODEOWNER (e.g. "respond
     to review requests within a week, help triage labelled issues").
   - (Optional) An [ORCID](https://orcid.org/) linked to your GitHub account.
3. Existing CODEOWNERS of the area (or, if none, `@linkml/core-team`) review
   the PR. Rough consensus is sufficient.

### PR description template

```markdown
## Request: add myself as CODEOWNER for <area>

**Path(s) added:** <e.g. packages/linkml/src/linkml/generators/pydanticgen/>

### Merged PRs justifying codeownership

- #<pr-number> — <short description>
- #<pr-number> — <short description>
- #<pr-number> — <short description>

### What I will do as a CODEOWNER

<e.g. "Respond to review requests within a week, help triage issues labeled
`generator-pydantic`, mentor new contributors to this area.">

### ORCID (optional)

<https://orcid.org/XXXX-XXXX-XXXX-XXXX>
```

## Stepping down

CODEOWNER status is a role, not a possession. It is picked up and put down as
circumstances and the project change.

**Voluntary stepping down.** If you no longer have capacity to review in an
area, open a PR removing yourself from `CODEOWNERS`. No justification
required. You can always be added back later.

**Inactivity.** If a CODEOWNER becomes unresponsive over an extended period,
an admin or a core developer may open a PR to remove them, with prior notice.
This is not a punishment — it is hygiene. The goal of the file is to route
reviews to *active* owners.

**Realignment with project direction.** Occasionally, a CODEOWNER's vision
for an area diverges materially from where the wider LinkML project is going,
and case-by-case [project-direction overrides](#when-project-direction-and-a-codeowner-disagree)
become a poor substitute for a clear stewardship arrangement. When this
happens, the preferred outcome is a conversation: clarify the design
principle in question, look for an arrangement that respects both the
CODEOWNER's expertise and the project's direction, and update governance
documents if the underlying disagreement points to something that should be
written down. If alignment cannot be restored, the core team may, after
explicit discussion with the person involved, open a PR to remove them as
CODEOWNER for that area. The intent is realignment of formal sign-off, not
removal of the person from the project — their expertise and past
contributions are not erased, and they remain a valued contributor who can
continue to review and advise informally.

## Editing the CODEOWNERS file

- All edits to `CODEOWNERS` go through a PR.
- PRs to `CODEOWNERS` themselves are owned by the core team and admins (this
  is itself encoded in the file).
- Keep the file sorted and grouped by area, with comments explaining each
  block. Readability matters — this file is documentation as much as it is
  configuration.

## Related documents

- [Contributor Hierarchy](contributor-hierarchy.md) — the four-tier structure
  and ascent process
- [Generator and Validator Governance](generator-governance.md) — contributor
  history used to seed per-generator ownership groups
- GitHub docs on [CODEOWNERS syntax](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners#codeowners-syntax)
