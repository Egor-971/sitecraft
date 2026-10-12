# Sitecraft validation

Release: 1.3.0. Date: October 12, 2026. Five skills, MIT license.

## Package verification

The release includes standard-library package tests, strict YAML/official JSON Schema validation, skill metadata checks, and a deterministic archive builder. Validation checks entrypoints, portable/compatible manifests, marketplace paths, local links, runtime license, malformed input diagnostics and excluded private materials. Archive tests cover reproducibility, file contents, exclusions, symlinks and accidental credential-like literals. These checks do not prove application design quality or comprehensive security.

After the English metadata/entrypoint update: strict package validation passed, all 15 package/archive tests passed, and all five Skill Creator checks passed. The official Codex CLI installed version 1.3.0; all 27 installed runtime files matched source SHA-256 hashes. Installed/enabled state is checked separately through the CLI listing. Strict validation uses PyYAML 6.0.3, jsonschema 4.26.0 and the [Agent Plugins schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json).

## Independent behavior trials

Two isolated requests were implemented using the 1.3 candidate instructions, before the English entrypoint translation:

| Request | Observed checks | Internal findings and corrections |
| --- | --- | --- |
| Fictional fashion shop | Search/filter, explicit size/color/stock, persistent cart, quantities, local test order, empty/unavailable states, keyboard and Console | Quantity rerender lost keyboard focus; corrected and retested |
| Fictional English tutor | Lesson format, Moscow schedule, validation, local inquiry, draft/confirmation recovery, keyboard and Console | Selected time lost on draft restore; date changed in UTC; editing an earlier inquiry restored old confirmation. Corrected and retested |

Five targeted Node tests passed across the two fixtures. The initial implementations were preserved separately from internal fixes. This is evidence about two requests, not a general success-rate estimate. The translated entrypoints and final QA additions have not had another independent behavioral trial; only the resulting package checks are reported for that revision.

The reviewer actually viewed initial/final first screens at 1280 × 720 and in a 390 × 844 CSS iframe viewport, plus product, cart, order, calendar and inquiry states. Browser resizing did not yield the requested mobile size; the iframe method was used and measured at 390 CSS pixels. It is responsive-layout evidence, not a physical phone or real-touch test. No material clipping was found in viewed states. The catalog illustrations are schematic demo assets, not photography suitable for a production fashion campaign. The tutor uses a familiar editorial treatment; these examples do not establish leader-level originality for every output.

The independent worker could not capture images in its browser context, so its DOM checks are distinct from the reviewer's actual screenshot inspection. Console warning/error lists were empty in the reviewed core journeys.

Fixtures, full browser logs, initial source snapshots and screenshots remain local. They are not bundled as product examples or public user data. No actual payments, customers, lessons, external messages or production accounts were used.

## Coverage and limits

Stored research records distinguish accessible live pages, official documentation, provided screenshots and blocked sources. Exact measurements have their own conditions in the [design study](../plugins/sitecraft/references/measured-design-study.md) and [product study](../plugins/sitecraft/references/measured-product-study.md). Some regional sites could not be loaded; no measurements or interactions are invented for them.

The [24 evaluation scenarios](evaluation-scenarios.md) are a future coverage plan, not 24 passed tests. Unverified: every other product sector, the professional-stage consent workflow on a separate project, all devices, physical touch, complete accessibility, real external integrations, field Core Web Vitals, conversion outcomes and guaranteed first-attempt quality. The plugin does not identify authorship or switch models.

Earlier versions 1.0/1.1/1.2 had 7/8/9 structural tests respectively and local CLI installation checks. Their historical research is retained as supporting notes; raw private conversation and uploaded reference images are excluded.

## Reproduce package checks

```sh
python3 scripts/validate_plugin.py
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py --output-dir dist
```

Strict mode additionally requires the dependencies in `requirements-dev.txt`. The [initial public CI run](https://github.com/Egor-971/sitecraft/actions/runs/38303390463) for commit `2c78528` passed on Python 3.12 and 3.14, including strict validation, all 15 tests and archive creation. Later commits have their own run status. Public repository: [Egor-971/sitecraft](https://github.com/Egor-971/sitecraft). Publication does not imply inclusion in a general plugin directory or endorsement by Anthropic, OpenAI or Google.
