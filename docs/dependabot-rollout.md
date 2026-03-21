# Dependabot Rollout Playbook

Use this playbook when switching a repository from Renovate to Dependabot and keeping PR volume low enough that each merge does not trigger unnecessary deployment churn.

## Recommended default

- Use Dependabot for npm and GitHub Actions updates.
- Group non-major version updates into one PR per ecosystem.
- Keep major updates separate.
- Keep only one open version-update PR per ecosystem at a time.
- Keep security updates enabled and grouped.
- Run checks weekly unless the repository is especially sensitive or high churn.

## Repo-side files

Commit a `.github/dependabot.yml` with at least:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "Europe/Zagreb"
    labels:
      - "dependencies"
    open-pull-requests-limit: 1
    groups:
      npm-non-major:
        applies-to: version-updates
        patterns:
          - "*"
        update-types:
          - "minor"
          - "patch"
      npm-security:
        applies-to: security-updates
        patterns:
          - "*"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:15"
      timezone: "Europe/Zagreb"
    labels:
      - "dependencies"
    open-pull-requests-limit: 1
    groups:
      github-actions-non-major:
        applies-to: version-updates
        patterns:
          - "*"
        update-types:
          - "minor"
          - "patch"
      github-actions-security:
        applies-to: security-updates
        patterns:
          - "*"
```

If the repository already has Renovate configured, remove `renovate.json` or `.renovaterc*` and disable the Renovate app for that repository in GitHub.

Why `open-pull-requests-limit: 1`:

- It serializes updates within each ecosystem.
- It avoids grouped non-major PRs competing with separate major PRs for the same lockfile.
- It reduces rebase churn and conflict noise.
- It is a better default for smaller repos where each merge can trigger a deployment or image rebuild.

## GitHub-side settings

Enable these repository settings:

- Dependency graph
- Dependabot alerts
- Dependabot security updates
- Grouped security updates
- Dependabot version updates
- Dependabot malware alerts

Recommended preset rule:

- Enable `Dismiss low-impact alerts for development-scoped dependencies` for private repositories.

Usually leave this preset disabled:

- `Dismiss package malware alerts`

Reason:

- Malware alerts are rare and high-signal enough that auto-dismiss is usually the wrong default.

## Existing PR cleanup

After merging the new `dependabot.yml`:

1. Close old Renovate PRs.
2. Close stale ungrouped Dependabot PRs.
3. Wait for Dependabot to rescan and recreate grouped PRs.

If a grouped PR and a major PR are already open for the same ecosystem:

1. Pick one path first.
2. Merge or close that PR.
3. Let Dependabot recreate or rebase the other one afterward.

## GitHub Actions scope

`github-actions` updates are separate from `npm` updates.

That means:

- npm dependency PRs are grouped together.
- workflow action version PRs are grouped together.
- they do not combine into one cross-ecosystem PR.

This is normal Dependabot behavior and usually the right tradeoff.

## Repeating this across repositories

The simplest reliable approach is:

1. Keep this file as the template.
2. Copy `.github/dependabot.yml` into each repo.
3. Manually verify the GitHub settings once per repo.

If you want to automate rollout across many repositories, use one of these:

- A small script that copies the config file, opens a branch, commits, pushes, and opens a PR with `gh`.
- Terraform or GitHub API automation for organization-level security settings.

## Notes on `gh`

Using `gh` is good for repository file changes and pull requests.

Typical use:

1. Create a branch.
2. Copy in `.github/dependabot.yml`.
3. Remove Renovate config if present.
4. Commit and push.
5. Open a PR.

Be cautious about assuming `gh` alone is enough for all security settings. Some repository and organization security settings are better managed through GitHub settings pages, API calls, or infrastructure-as-code rather than ad hoc local commands.
