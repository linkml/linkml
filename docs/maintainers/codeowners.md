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
down (see [How to step down](#how-to-step-down)) or adding co-owners so that
review is not dependent on a single person.

### Implementation note

GitHub's branch protection cannot enforce a time-based fallback automatically:
if "Require review from Code Owners" is enabled, CODEOWNER approval is
required indefinitely. To make this policy effective in GitHub's UI, an
[admin](contributor-hierarchy.md) may temporarily remove the CODEOWNER
requirement for a specific PR once the month has elapsed, or the policy may
be encoded in a bot in the future. Until then, the policy is honour-based:
core developers should invoke it sparingly and transparently.

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

## How to step down

If you no longer have capacity to review in an area, open a PR removing
yourself from `CODEOWNERS`. No justification required. You can always be added
back later.

If a CODEOWNER becomes unresponsive, an admin or a core developer may open a
PR to remove them, with prior notice. This is not a punishment — it is
hygiene. The goal of the file is to route reviews to *active* owners.

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
