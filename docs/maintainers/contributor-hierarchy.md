# Contributor Hierarchy

LinkML uses a lightweight four-level contribution structure. It exists to make
expectations, permissions, and growth paths transparent across all LinkML
repositories.

The goal is not gatekeeping — the goal is to make it obvious **how people grow
into responsibility over time**, and to ensure that every PR has a clear path to
review and merge.

## Overview

| Level | Team | Write access | Can merge? | Required reviewer? |
| --- | --- | --- | --- | --- |
| 1. Community contributor | — | No (forks only) | No | No |
| 2. Collaborator | [`developers-collaborators`](https://github.com/orgs/linkml/teams/developers-collaborators) | Broad write | Only in areas where they are a CODEOWNER | Only in CODEOWNER areas |
| 3. Core developer | [`core-team`](https://github.com/orgs/linkml/teams/core-team) | Broad write | Yes (within branch protection) | Only where explicitly listed in CODEOWNERS |
| 4. Admin | [`admin`](https://github.com/orgs/linkml/teams/admin) | Admin | Yes | Only where explicitly listed in CODEOWNERS |

Team URLs are only visible to members of the LinkML GitHub organization.

---

## 1. Community contributor

**The default and most important entry point.** Zero friction.

Typical characteristics:

- Not (yet) deeply embedded in the LinkML ecosystem
- Works via forks
- Not part of any GitHub team
- No need to request membership or permission to open PRs

If you want to fix a bug, file an issue, or suggest an improvement — just do it.
You do not need to be on any team.

## 2. Collaborator

Team: [`developers-collaborators`](https://github.com/orgs/linkml/teams/developers-collaborators)

**Regular contributors** who are trusted with broad write access across LinkML
repos, but are not expected to merge arbitrary changes.

Capabilities:

- Broad write access across many LinkML repos
- Cannot merge by default
- May request [CODEOWNERS](codeowners.md) status for specific areas they
  maintain (e.g., a generator)
- Once listed as a CODEOWNER for an area, may review and approve PRs in that
  area

Expectations:

- Respond to feedback and change requests on your own PRs in a reasonable
  timeframe
- Be a good citizen: follow the [code of conduct](code-of-conduct.md) and the
  [contribution guidelines](contributing.md)

## 3. Core developer

Team: [`core-team`](https://github.com/orgs/linkml/teams/core-team)

**People actively stewarding LinkML as a whole.**

Capabilities:

- All collaborator capabilities
- Can review and approve PRs anywhere in the monorepo (team write access is
  sufficient; CODEOWNER approval is only required for paths explicitly listed
  in the [CODEOWNERS](codeowners.md) file)
- May invoke the [1-month CODEOWNER fallback](codeowners.md#avoiding-review-bottlenecks-the-1-month-fallback)
  to approve stalled PRs in areas with unresponsive CODEOWNERS
- Still subject to branch protection rules (cannot force-push, etc.)

Expectations:

- Participate in LinkML developer calls
- Help triage issues and review PRs across the project, not just your own
  patches
- Mentor collaborators and community contributors

## 4. Admin

Team: [`admin`](https://github.com/orgs/linkml/teams/admin)

**Small group responsible for repo-level governance.**

Capabilities:

- Manage GitHub organization and repository settings
- Adjust branch protection rules when necessary
- Manage team membership

Admins are typically appointed by existing admins as responsibility transitions
over time. There is no formal democratic process, but the group is intentionally
small and accountable to the core team.

---

## How to ascend

Progression is **contributor-initiated, not top-down**. You ask; existing
members review.

### Community contributor → Collaborator

1. Have roughly **three merged PRs** across any LinkML repository.
   The number is a soft floor, not a hard rule — the point is to demonstrate
   sustained engagement and familiarity with the review process.
2. Open an issue in [`linkml/linkml`](https://github.com/linkml/linkml/issues/new)
   requesting collaborator status. Include:
   - Links to the merged PRs
   - A short note on what areas you expect to contribute to
   - (Optional but encouraged) an [ORCID](https://orcid.org/) linked to your
     GitHub account — this helps with long-term attribution across the
     dependency graph
3. A member of the core team or admin will review and add you to the
   `developers-collaborators` team if approved.

### Collaborator → CODEOWNER for a specific area

See [CODEOWNERS](codeowners.md) for the full process. In short: demonstrate
sustained, quality contributions to a specific area (generator, validator,
subsystem), then **open a PR** adding yourself to `.github/CODEOWNERS` for
that path. The PR description must link to **at least three merged PRs** in
that area that justify codeownership.

### Collaborator → Core developer

1. Sustained contribution over time. As a soft guideline:
   - Roughly **~10 merged PRs**
   - Regular review activity (a rough target: ~1 completed issue + ~2 PR
     reviews per week, sustained over several weeks)
   - Intent to participate in LinkML developer calls
2. Open an issue requesting core developer status, linking to your contribution
   and review history.
3. The existing core team discusses and — if there is rough consensus — an
   admin adds you to the `core-team` team.

### Core developer → Admin

Admin status is not requested; it is offered. When an existing admin needs to
step back, or when the project's administrative load grows, the existing admins
invite a core developer to take on the role. If you have thoughts on who should
be an admin, raise them in a governance issue.

---

## Stepping back

Contributing to LinkML is voluntary. If your circumstances change and you need
to reduce your involvement, that is fine and expected. Open an issue or ping an
admin and we will move you to a level that matches your current capacity. You
can always come back.

Admins may also periodically review team membership and move inactive members to
a lower tier, with notice. The intent is to keep the active teams reflective of
who is actually engaged, not to penalize anyone.

---

## Related documents

- [CODEOWNERS](codeowners.md) — who reviews what, and how to be added
- [Generator and Validator Governance](generator-governance.md) — contributor
  history per generator, used as a baseline for forming CODEOWNER groups
- [Contribution Guidelines](contributing.md) — day-to-day contribution process
- [Code of Conduct](code-of-conduct.md)
