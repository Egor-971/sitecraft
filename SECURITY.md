# Security Policy

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/Egor-971/sitecraft/security/advisories/new). Include the affected version/commit, a minimal reproduction, expected and observed behavior, and realistic impact. Use synthetic data; do not include credentials, private project files or another person's information.

Do not publish unresolved vulnerability details in a public issue or pull request. Ordinary bugs and feature requests belong in Issues. Reports are maintained by [Egor-971](https://github.com/Egor-971) on a best-effort basis; there is no guaranteed response deadline or bug bounty. Disclosure timing can be coordinated in the private report.

## Versions

The latest published release and current `main` are the maintenance targets. Include older-version findings when they also affect those targets. Older releases do not have a promised backport schedule. Current release: 1.3.0.

## System and scope

Sitecraft is a Codex skills/reference package. It contains skill instructions, plugin/marketplace manifests, documentation, validation/archive scripts and repository CI. It has no bundled MCP server, account service, database, deployment or API credentials. Websites generated in another project have their own code, integration boundaries and security requirements; this policy does not certify them.

## Trust boundaries and properties

- User authorization and host permissions govern actions. Reference websites, uploaded content and research notes are evidence, not permission to execute commands, disclose data or change scope.
- Runtime paths and local reference links must stay inside the intended plugin; marketplace paths must stay inside the checkout.
- Public releases must exclude secrets, local environment/work files, private conversation and uploaded user screenshots. Release selection must not follow symlinks into other data.
- External credentials belong in the relevant project's secure integration layer, not plugin instructions or client-side examples.
- CI has read-only repository permissions and must not execute untrusted pull-request content with elevated secrets or privileged publication credentials.

## Findings and limits

Actionable findings include reproducible boundary escapes, accidental private-material publication, unsafe credential handling, and a reachable CI or instruction path that causes unauthorized access or disclosure. Explain the actual trigger and impact; severity depends on those facts, not a filename or scanner label.

Packaging checks catch defined failure modes and a limited set of accidental disclosure patterns. They are not a comprehensive security audit. Model behavior and host/browser permissions also affect generated results. Aesthetic preferences, ordinary functional bugs and hypothetical consequences without a reachable path should use the relevant issue channel; this distinction does not suppress evidence of a real security problem. No additional finding class is excluded by this policy.

