# Sitecraft

Codex skills for distinctive websites and functional web products, built around a real business goal.

[Русский](docs/README.ru.md) · [Validation](docs/VALIDATION.md) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md)

Sitecraft helps Codex choose an identity from the product, audience and content, then implement and inspect the actual user journey. It supports new sites, existing interfaces, visual audits and professional UI/UX upgrades. It preserves the user's stack and useful functionality.

## Five focused skills

| Skill | Use it for |
| --- | --- |
| `$sitecraft-create` | A new website, landing page or public product page |
| `$sitecraft-product` | The application itself: shops, chats, learning, media and working tools |
| `$sitecraft-redesign` | Redesign while preserving routes, data and integrations |
| `$sitecraft-review` | Evidence-based review of a screenshot, live interface or code |
| `$sitecraft-elevate` | An explicitly requested or approved professional design direction |

```text
Use $sitecraft-product. Build a shop in this repository.
The goal is finding and ordering a suitable available product.
Research relevant competitors, create an individual design system,
implement the full scoped journey and verify it in the browser.
Keep the existing stack and state the actual integration boundaries.
```

Skill entrypoints and plugin UI are in English. Site output follows the audience's language and locale; historical supporting research notes include Russian-language observations. Each skill supports implicit discovery; an explicit invocation is useful for the first trial.

## Install from a checkout

Clone the public repository, then run from its root:

```sh
git clone https://github.com/Egor-971/sitecraft.git
cd sitecraft
```

```sh
codex plugin marketplace add .
codex plugin add sitecraft@sitecraft-marketplace
codex plugin list --marketplace sitecraft-marketplace --json
```

The source contains a portable `plugin.json`, a compatible `.codex-plugin/plugin.json` and a local marketplace. Installation commands were tested with the author's Codex CLI. Client interfaces can vary. A newly installed version can be tried in a fresh chat.

## What changes the result

- **Purpose first.** A shop needs choice and ordering; a translator needs input and output; a marketing page needs a clear offer and action. The plugin distinguishes these outcomes.
- **A direction before implementation.** Composition, density, type, color and materials follow the brief. The initial direction is checked for interchangeable defaults before significant implementation.
- **Relevant research.** Usually 2–4 current competitors and their accessible core screens, with URLs, conditions and limits. Stored brand and sector studies provide context without replacing fresh research.
- **Useful components.** Cards, tables, filters, icons and player controls are allowed when they support the task. There is no compulsory font, palette, hero or section template.
- **A checked first delivery.** Run the implementation, test the core journey, inspect relevant wide/narrow states, keyboard behavior, screenshots and errors, then fix material defects before handoff.
- **Honest boundaries.** A mock is identified as a mock; a local demo does not prove payments, AI, multi-user synchronization or production readiness.

There are [24 product profiles](plugins/sitecraft/references/product-patterns.md), including commerce and marketplaces, communication, learning, media, workspaces and financial interfaces. Unlisted niches use the same goal-and-journey process. Profiles are guidance, not finished application templates or automatic authorization to add every feature.

## Recommendations and evidence

[Official guidance](plugins/sitecraft/references/official-guidance.md) records the relevant Anthropic, OpenAI and Google/web.dev sources and how they inform this plugin. These organizations do not endorse or certify Sitecraft. Recommendations are adapted to the user's brief and existing design system.

The [first-delivery protocol](plugins/sitecraft/references/first-delivery.md) separates the initial implementation, internal fixes and delivered result. [Validation](docs/VALIDATION.md) distinguishes package tests, behavioral trials and actual visual observations. A passing packaging test does not demonstrate the quality of an application.

Sitecraft reduces generic generated-UI defaults; it does not detect authorship or guarantee an ideal result on every first attempt. It does not switch models or reasoning settings. Research of another company's UI does not prove its hidden workflows.

## Develop and build an archive

Basic validation uses the Python standard library:

```sh
python3 scripts/validate_plugin.py
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py --output-dir dist
```

Strict validation also parses YAML and checks the official plugin schema:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_plugin.py --strict
```

The archive builder selects public source directories, excludes local environment/work files, rejects raw conversation archives and symlinks, checks a limited set of accidental disclosure patterns, verifies the archive contents and produces a SHA-256 file. This is a packaging check, not a comprehensive security audit. GitHub CI is configured to validate and build the archive; its actual execution status is recorded separately.

## License and project boundaries

[MIT](LICENSE). Maintained by [Egor-971](https://github.com/Egor-971).

This is a skills-and-reference package for Codex. It has no bundled MCP server, hooks, external accounts or API keys. The agent needs project access, a suitable execution environment and browser tooling for runtime/visual verification. Real external functions require their own implementation and access.

Third-party websites are referenced through links and original observations. Their images, fonts, logos and source skills are not relicensed by this repository. Raw private conversation and user screenshots are excluded from this public package. Publishing this repository does not itself mean inclusion in a general plugin directory.
