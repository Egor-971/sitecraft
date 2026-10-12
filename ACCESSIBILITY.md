# Accessibility

Sitecraft aims to help agents create interfaces people can understand and operate with different input methods and access needs. This is a project commitment and a description of current limits, not a WCAG certification.

## Scope

The plugin distributes text instructions, metadata and development scripts. It does not supply a finished website component library or control Codex's own interface. A generated site's accessibility depends on its implementation, content, integrations and actual verification.

The [QA guidance](plugins/sitecraft/references/qa.md) asks for semantic controls, accessible names, visible and logical keyboard focus, readable localized text, contrast checks, responsive layouts, reduced-motion alternatives and reachable actions. Substantial work requires browser and visual inspection with recorded conditions. Report what was actually tested.

## Current evidence and limits

Package CI runs on Python 3.12 and 3.14. Two local behavior trials included keyboard paths and browser inspection; their narrow visual review used a 390-pixel CSS iframe viewport. They were not physical-device, screen-reader or comprehensive accessibility audits. No assistive-technology compatibility matrix or blanket conformance claim is available. Historical supporting research notes include Russian; primary skill entrypoints and release documentation are English. Site language follows its audience.

## Report a barrier

Open an [accessibility issue](https://github.com/Egor-971/sitecraft/issues/new?template=accessibility.yml). Describe the affected skill/page, version, environment or assistive technology, steps, expected behavior and observed barrier. Sanitized screenshots or recordings are welcome but optional. Do not upload personal or confidential data. Reports are reviewed by [Egor-971](https://github.com/Egor-971) on a best-effort basis.

