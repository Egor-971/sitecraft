---
name: sitecraft-product
description: "Build or substantially redesign a functional web application around its business goal, complete user journeys and data. Use for shops, chats, learning, media or working tools rather than their promotional pages."
---

# Sitecraft: build a web product

Implement the product within the authorized scope: buying, learning, communicating, watching, listening, editing or another requested outcome. Translate "leader-level quality" into observable qualities, without promising a competitor's entire infrastructure. Use the audience's language and locale.

For substantial work, read the [product workflow](../../references/product-workflow.md) and [first delivery](../../references/first-delivery.md). Find and read only applicable sections of the [profiles](../../references/product-patterns.md), [design rules](../../references/design-rules.md) and [QA](../../references/qa.md). [Sector research](../../references/sector-research.md) and [official guidance](../../references/official-guidance.md) support concrete decisions, without requiring a full archive read.

## Work

1. Inspect the project, instructions, stack and existing functionality. Establish audience, roles, goal, primary journey and acceptance criteria. Distinguish a promotional site, application and combination. Do not repeat answered questions or silently reduce a complete request to a prototype.
2. Usually research 2–4 current comparable products: accessible screens and core journey, composition, density, copy, materials, type roles, spacing and states. Record sources, conditions and limits; do not invent measurements when access is blocked.
3. Define routes, data, persistence, permissions and integrations. Connect an original design system to the task and check the direction before code. Workspaces, catalogs, composers and players may need different densities. Keep useful cards and tools.
4. Implement the requested functionality and state on the chosen stack. Address semantics, keyboard controls, responsive layouts, stale responses and recovery. Select meaningful checks based on data/action risks. Give external services a real integration boundary and keep secrets server-side. Label mocks clearly.
5. Run and complete the entire primary path: action → result → refresh/return, important errors and recovery. Actually inspect screenshots and Console; test narrow layouts and keyboard controls. Fix material defects before handoff and retest affected paths. A build and a single screenshot do not finish an application.

## Handoff

Record goals/criteria, references, decisions, routes/roles/data, integration mode, actual commands, QA and remaining work in `docs/design/SITECRAFT.md`. Deliver working source with precise boundaries. Do not call a local simulation real payment, AI inference, delivery, collaboration or banking. Continue independent work when an external service is blocked.

Baseline quality belongs to this skill. An explicit professional UI/UX request authorizes [sitecraft-elevate](../sitecraft-elevate/SKILL.md) without repeated consent; an optional later stage follows the [proposal protocol](../../references/design-upgrade.md). Installing a plugin does not authorize publication, external transactions or changes to another project.
